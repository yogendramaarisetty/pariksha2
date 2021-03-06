# Generated by Django 3.0 on 2020-07-16 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('mobile_number', models.CharField(max_length=12)),
                ('college', models.CharField(blank=True, max_length=100)),
                ('roll_number', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=120)),
                ('pin', models.CharField(max_length=8)),
                ('description', models.TextField()),
                ('duration', models.DurationField()),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CodeDraft',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.TextField()),
                ('candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Candidate')),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Challenge')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tinput', models.TextField()),
                ('toutput', models.TextField()),
                ('hint', models.CharField(max_length=50)),
                ('sample', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('passed_cases', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('code_draft', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.CodeDraft')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionLanguageDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Language')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Question')),
            ],
        ),
        migrations.AddField(
            model_name='codedraft',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Language'),
        ),
        migrations.AddField(
            model_name='codedraft',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Question'),
        ),
        migrations.CreateModel(
            name='CandidateChallenge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('suspicious_count', models.IntegerField(default=0)),
                ('completed_status', models.BooleanField(default=False)),
                ('candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Candidate')),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Challenge')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='codedraft',
            unique_together={('challenge', 'question', 'candidate', 'language')},
        ),
        migrations.CreateModel(
            name='ChallengeQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Challenge')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Question')),
            ],
            options={
                'unique_together': {('challenge', 'question')},
            },
        ),
        migrations.CreateModel(
            name='ChallengeLanguages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Challenge')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='challenge.Language')),
            ],
            options={
                'unique_together': {('challenge', 'language')},
            },
        ),
    ]
