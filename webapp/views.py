import encodings
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect,render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
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
class Login(UserPassesTestMixin, LoginView):
    template_name = "webapp/login.html"
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("app_webapp:home")


class Home(LoginRequiredMixin, ListView):
    template_name = "webapp/home.html"
    context_object_name = "csvs"
    paginate_by = 20
    def get_queryset(self):
        return CSVModel.objects.all()
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
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
        objs = CSVModel.objects.filter(id__in=ids).values_list("full_name","gender","salary","designation","added_by__username","added_on__date")
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
class Logout(LoginRequiredMixin, LogoutView):
    pass
