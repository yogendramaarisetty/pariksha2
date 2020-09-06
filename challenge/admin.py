from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import JudgeApiKey,Candidate,Challenge,Question,ChallengeLanguages,Language,ChallengeQuestion,CandidateChallenge,QuestionLanguageDefault,Submission,TestCase,CodeDraft,SampleLanguageCodes
admin.site.register(Candidate)
class questionInline(admin.StackedInline):
    model = ChallengeQuestion
class ChallengeAdmin(admin.ModelAdmin):
    inlines = [
        questionInline,
    ]
admin.site.register(Challenge,ChallengeAdmin)

class testcaseInline(admin.TabularInline):
    model = TestCase

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        testcaseInline,
    ]
class ApiKeyAdmin(admin.ModelAdmin):
    list_display  = ('name','active')
admin.site.register(Question,QuestionAdmin)
admin.site.register(ChallengeLanguages)
admin.site.register(Language)
admin.site.register(ChallengeQuestion)
admin.site.register(CandidateChallenge)
admin.site.register(QuestionLanguageDefault)
admin.site.register(Submission)
admin.site.register(TestCase)
admin.site.register(CodeDraft)
admin.site.register(SampleLanguageCodes)
admin.site.register(JudgeApiKey,ApiKeyAdmin)

