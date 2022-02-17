from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .validators import validate_DOB
GENDER_CHOICES = (
    ("1", "Female"),
    ("0", "Male"),
    ("2", "Other"),
)


class CSVModel(models.Model):
    full_name = models.CharField(max_length=40)
    date_of_birth = models.DateField(validators=(validate_DOB,),help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="1")
    salary = models.DecimalField(max_digits=9, decimal_places=2)
    designation = models.CharField(max_length=80)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cvsmodel",related_query_name="has_uploaded")
    added_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ("-added_on",)
        verbose_name_plural = "CSVs"
