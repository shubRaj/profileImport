# Generated by Django 4.0.2 on 2022-02-17 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_alter_csvmodel_date_of_birth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvmodel',
            old_name='Designation',
            new_name='designation',
        ),
    ]