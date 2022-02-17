from django import forms

class CSVForm(forms.Form):
    CSV_FILE = forms.FileField()