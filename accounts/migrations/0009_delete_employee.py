# Generated by Django 4.0.3 on 2022-04-20 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_employee_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
