# Generated by Django 3.0.8 on 2020-09-03 11:33

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0015_judgeapikey_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
