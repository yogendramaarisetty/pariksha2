# Generated by Django 3.0 on 2020-07-17 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0005_testcase_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleLanguageCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Language')),
            ],
        ),
    ]
