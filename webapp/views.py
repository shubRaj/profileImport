from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect,render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView
from .models import CSVModel
from .forms import CSVForm,CSVModelForm
from django.db import IntegrityError
from .extractors import getFromCSV, getFromXLS

class Login(UserPassesTestMixin, LoginView):
    template_name = "webapp/login.html"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("app_webapp:home")


class Home(LoginRequiredMixin, ListView):
    template_name = "webapp/home.html"
    context_object_name = "csvs"

    def get_queryset(self):
        return CSVModel.objects.all()

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
                        # csv_instance.save()
                else:
                    skipped.append(i)
            if skipped:
                form.add_error("__all__",f"{len(skipped)} rows {skipped} were skipped since they did not have data")
            kwargs.update({"form":form})
        return super().get(request, *args, **kwargs)


class Logout(LoginRequiredMixin, LogoutView):
    pass
