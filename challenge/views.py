from django.shortcuts import render,redirect
from .models import Candidate,Challenge,Question,SampleLanguageCodes,ChallengeLanguages,Language,ChallengeQuestion,CandidateChallenge,QuestionLanguageDefault,Submission,TestCase,CodeDraft
import json,requests
from .forms import CandidateForm,SampleLanguageCodeForm
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404
from django.core import serializers
from django.contrib import messages 
from django.contrib.auth.decorators import user_passes_test
from .coderun_api import coderun_api
global user_data
user_data = {'name':'','picture':''}
def get_user_data(request):
    json_data = {
    'name':'Administrator',
    'picture':'https://www.pngfind.com/pngs/m/528-5286002_forum-admin-icon-png-nitzer-ebb-that-total.png'
    }
    current_user = SocialAccount.objects.filter(user=request.user).first()
    try:
        json_data = current_user.extra_data
    except:
        pass
    return json_data

def home(request):
    user_data = {'name':'','picture':''}
    if request.user.is_authenticated:
        user_data = get_user_data(request)
    context = {'title':'home','username':user_data['name'],'profile_pic':user_data['picture']}
    if request.method == 'POST':
        pin = request.POST.get('pin')
        challenge = Challenge.objects.filter(pin=pin).first()
        if challenge != None:
            return redirect('candidate_details',challenge_id=str(challenge.id))
        else :
            context['error'] = "Invalid PIN"
    return render(request,"home.html",context)


def sample_language_codes(request):
    form = SampleLanguageCodeForm()
    return render(request,'sample_code.html',{'form':form})

@user_passes_test(lambda u: u.is_authenticated,login_url='google_login')
def candidate_details(request,challenge_id):
    
    if request.user.is_authenticated:
        user_data = get_user_data(request)
    else:
        return redirect('home')
        
    candidate = Candidate.objects.filter(user=request.user).first()
    if candidate !=None:
        return redirect('instructions',challenge_id=str(challenge_id),candidate_id = str(candidate.id))
    elif request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.save()
            candidate_challenge = CandidateChallenge()
            candidate_challenge.candidate = candidate
            candidate_challenge.challenge = Challenge.objects.get(pk=challenge_id)
            candidate_challenge.save()
            return redirect('instructions',challenge_id=str(challenge_id),candidate_id = str(candidate.id))
        return render(request,'candidate_form.html')
    else:
        form = CandidateForm()
        return render(request,'candidate_form.html',{'form':form,'username':user_data['name'],'profile_pic':user_data['picture']})

@user_passes_test(lambda u: u.is_authenticated,login_url='google_login')
def instructions(request,challenge_id,candidate_id):
    if request.user.is_authenticated:
        user_data = get_user_data(request)
    challenge = Challenge.objects.get(pk = challenge_id)
    candidate = Candidate.objects.filter(user = request.user).first()
    challenge_questions = ChallengeQuestion.objects.filter(challenge = challenge)
    candidate_id = str(candidate.id)
    challenge_id = str(challenge.id)
    return render(request,"instructions.html",{'title':'Instructions','challenge':challenge,'question':challenge_questions,'candidate_id':candidate_id,'challenge_id':challenge_id,'username':user_data['name'],'profile_pic':user_data['picture']})

def check_valid_user_candidate(request,candidate_id):
    candidate = Candidate.objects.get(pk=candidate_id)
    return candidate.user == request.user

def get_candidate_codes(candidate,challenge,question):
    languages = Language.objects.all()
    code_drafts = CodeDraft.objects.filter(candidate=candidate).filter(challenge=challenge).filter(question=question)
    candidate_codes = {'question':question.title,
                            'qid':str(question.id)}
    if len(code_drafts) == 0:
        codes = {}
        for l in languages:
            c = CodeDraft.objects.create(candidate=candidate,challenge=challenge,question=question,language=l)
            default_code = QuestionLanguageDefault.objects.filter(question=question).filter(language = l).first()
            if default_code == None:
                sample_code = SampleLanguageCodes.objects.filter(language = l).first()
                if sample_code != None:
                    c.code = sample_code.code
                else:
                    c.code = ""
                c.save()
            else:
                c.code = default_code.code
                c.save()
            codes[l.value] = c.code
        candidate_codes['codes'] = codes
    else:
        codes = {}
        q_dict = CodeDraft.objects.filter(candidate=candidate).filter(challenge=challenge).filter(question = question)
        for el in q_dict:
            l = el.language
            codes[l.value] = el.code
        candidate_codes['codes'] = codes
    return candidate_codes
        
        
@user_passes_test(lambda u: u.is_authenticated,login_url='google_login')
def test_page(request,challenge_id,candidate_id):
    if not check_valid_user_candidate(request,candidate_id):
        return render(request,"error.html",{"msg":"this is not your test"})
    candidate,challenge  = Candidate.objects.get(pk=candidate_id),Challenge.objects.get(pk = challenge_id)
    challenge_questions = ChallengeQuestion.objects.filter(challenge=challenge)   
    if request.is_ajax():
        if request.method == 'POST':
            question,code,language = Question.objects.get(pk = request.POST.get('qid')),request.POST.get('code'),Language.objects.get(value = request.POST.get('language'))
            print(question,code ,language)
            output_response = coderun_api(code,language,"","","")
            res={'msg':'Code recieved success'}
            return HttpResponse(output_response, content_type="application/json")
        elif request.method == 'GET':
            question = Question.objects.get(pk =request.GET.get('qid') )
            candidate_codes = get_candidate_codes(candidate,challenge,question)
            return HttpResponse(json.dumps(candidate_codes), content_type="application/json")
    
    data = {
    'challenge':challenge,
    'questions':challenge_questions,
    'languages':Language.objects.all(),
    }
    return render(request,'test_page.html',data)
