from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import ListView,View
from .models import CSVModel
from .forms import CSVForm,CSVModelForm
from django.db import IntegrityError
from django.http import HttpResponse
from .extractors import getFromCSV, getFromXLS
import xlwt
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
class Login(UserPassesTestMixin,SuccessMessageMixin, LoginView):
    template_name = "webapp/login.html"
    success_message = "Login successful"
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("app_webapp:home")

class Home(LoginRequiredMixin, ListView):
    template_name = "webapp/home.html"
    context_object_name = "csvs"
    paginate_by = 20
    def get_queryset(self):
        uploader = self.request.GET.get("filter-by-uploader")
        order = self.request.GET.get("order-by")
        objs =  CSVModel.objects.all()
        if uploader:
            objs = objs.filter(added_by__username=uploader)
        if order and order.lower() in ("asc","desc"):
            if order.lower() == "desc":
                objs = objs.order_by("added_on")
        return objs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            csvFile = form.cleaned_data["csvfile"]
            csvPath = csvFile.temporary_file_path()
            csvs = getFromCSV(csvPath) if csvFile.content_type == "text/csv" else getFromXLS(csvPath)
            skipped = []
            for i,csv in enumerate(csvs,start=1):
                csvForm = CSVModelForm(csv)
                if [value for value in csv.values() if value]:
                    if csvForm.is_valid():
                        csv_instance = csvForm.save(commit=False)
                        csv_instance.added_by = self.request.user
                        csv_instance.save()
                else:
                    skipped.append(i)
            if skipped:
                form.add_error("__all__",f"{len(skipped)} rows {skipped} were skipped since they did not have data")
            kwargs.update({"form":form})
        return super().get(request, *args, **kwargs)

class Export(View):
    def post(self,request,*args,**kwargs):
        ids = [int(id) for id in request.POST.keys() if id.isnumeric()]
        if ids:
            objs = CSVModel.objects.filter(id__in=ids).values_list("full_name","gender","salary","designation","added_by__username","added_on__date")
        else:
            objs = CSVModel.objects.all().values_list("full_name","gender","salary","designation","added_by__username","added_on__date")
        if request.POST.get("type") == "xls":
            response = HttpResponse(content_type="text/ms-excel")
            response["Content-Disposition"]="attachment; filename=modelcsv.xls"
            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("CSVModel")
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ["full_name","gender","salary","designation","added_by","added_on"]
            for col_num in range(len(columns)):
                ws.write(row_num,col_num,columns[col_num],font_style)
            font_style = xlwt.XFStyle()
            rows = objs
            for row in rows:
                row_num+=1
                for col_num in range(len(row)):
                    ws.write(row_num,col_num,str(row[col_num]),font_style)
            wb.save(response)
            return response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"]="inline; attachment; filename=modelcsv.pdf"
        response["Content-Transfer-Encoding"] = "binary"
        html_string=render_to_string("webapp/pdf.html",{"csvs":objs})
        html=HTML(string=html_string)
        result = html.write_pdf()
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name,"rb")
            response.write(output.read())
        return response
class Logout(LoginRequiredMixin,LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'Successfully Logout',fail_silently=True)
        return response
