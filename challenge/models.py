import uuid
from django.contrib.auth.models import User
from django.db import models
from djrichtextfield.models import RichTextField
class Challenge(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=120)
    pin = models.CharField(max_length=8)
    description = models.TextField()
    duration = models.IntegerField()
    active = models.BooleanField()
    
    def __str__(self):
        return self.title

class Candidate(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=12)
    college = models.CharField(blank=True,max_length=100)
    roll_number = models.CharField(blank=True,max_length=100)
    def __str__(self):
        return self.full_name

class Question(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title=models.CharField(max_length=50)
    description= RichTextField()
    def __str__(self):
        return f'{self.title}'

class Language(models.Model):
    id=models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    value = models.CharField(blank=True, max_length=100)
    def __str__(self):
        return f'{self.name}'


class ChallengeQuestion(models.Model):
    class Meta:
        unique_together = [['challenge','question'],]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    challenge = models.ForeignKey(Challenge,on_delete=models.CASCADE,null=True)
    question  = models.ForeignKey(Question,on_delete=models.CASCADE,null=True)

class CandidateChallenge(models.Model):
    class Meta:
        unique_together = [['challenge','candidate'],]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    candidate= models.ForeignKey(Candidate,on_delete=models.CASCADE,null=True)
    challenge = models.ForeignKey(Challenge,on_delete=models.CASCADE,null=True)
    start_time = models.DateTimeField(blank=True,null=True,auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(blank=True,null=True,auto_now=False, auto_now_add=False)
    suspicious_count = models.IntegerField(default=0)
    completed_status = models.BooleanField(default=False)

class CodeDraft(models.Model):
    class Meta:
        unique_together = [['challenge','question','candidate','language'],]
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    candidate= models.ForeignKey(Candidate,on_delete=models.CASCADE,null=True)
    challenge = models.ForeignKey(Challenge,on_delete=models.CASCADE,null=True)
    question  = models.ForeignKey(Question,on_delete=models.CASCADE,null=True)
    language  = models.ForeignKey(Language,on_delete=models.CASCADE,null=True)
    code = models.TextField()

class QuestionLanguageDefault(models.Model):
    class Meta:
        unique_together = [['question','language'],]
    question  = models.ForeignKey(Question,on_delete=models.CASCADE,null=True)
    language  = models.ForeignKey(Language,on_delete=models.CASCADE,null=True)
    code = models.TextField()

class TestCase(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    tinput = models.TextField(blank=True)
    toutput = models.TextField(blank=True)
    hint = models.CharField(blank=True,max_length = 50)
    score = models.IntegerField(default=0)
    sample = models.BooleanField(default=False)
    def is_sample(self):
        return self.sample
class Submission(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    code_draft = models.ForeignKey(CodeDraft,on_delete=models.CASCADE,null=True)
    passed_cases = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

class ChallengeLanguages(models.Model):
    class Meta:
        unique_together = [['challenge','language'],]
    challenge = models.ForeignKey(Challenge,on_delete=models.CASCADE,null=True)
    language  = models.ForeignKey(Language,on_delete=models.CASCADE,null=True)

class SampleLanguageCodes(models.Model):
    language = models.ForeignKey(Language,unique=True, on_delete=models.CASCADE,null = True)
    code = models.TextField()

class Solution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    solution = models.TextField(blank=True)