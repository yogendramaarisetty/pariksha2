# Generated by Django 3.0 on 2020-07-18 17:13

from django.db import migrations, models
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0006_samplelanguagecodes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=djrichtextfield.models.RichTextField(),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='hint',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='tinput',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='toutput',
            field=models.TextField(blank=True),
        ),
    ]