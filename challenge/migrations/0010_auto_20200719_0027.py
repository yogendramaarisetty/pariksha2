# Generated by Django 3.0 on 2020-07-18 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0009_auto_20200719_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samplelanguagecodes',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Language', unique=True),
        ),
    ]
