# Generated by Django 2.2 on 2022-02-23 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_auto_20220223_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
