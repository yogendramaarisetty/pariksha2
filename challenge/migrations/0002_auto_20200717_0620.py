# Generated by Django 3.0 on 2020-07-17 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='candidatechallenge',
            unique_together={('challenge', 'candidate')},
        ),
    ]