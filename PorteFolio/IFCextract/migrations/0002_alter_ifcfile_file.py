# Generated by Django 4.2.3 on 2023-07-18 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IFCextract', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ifcfile',
            name='file',
            field=models.FileField(upload_to='ifc'),
        ),
    ]
