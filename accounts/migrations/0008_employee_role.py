# Generated by Django 4.0.3 on 2022-04-20 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('admin', 'ADMINISTRADOR'), ('client', 'CLIENTE'), ('worker', 'TRABAJADOR'), ('suplier', 'PROVEEDOR')], default='worker', max_length=50),
        ),
    ]
