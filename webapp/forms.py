from django import forms
from django.conf import settings
from .models import CSVModel
class CSVForm(forms.Form):
    csvfile = forms.FileField()
    def clean_csvfile(self):
        csvfile = self.cleaned_data["csvfile"]
        if not (csvfile.content_type in settings.FILE_CONTENT_TYPES):
            raise forms.ValidationError(f"Unsupported Content-Type:{csvfile.content_type}",code='unsupported')
        return csvfile
class CSVModelForm(forms.ModelForm):
    class Meta:
        model = CSVModel
        exclude = ("id","added_by","added_on")