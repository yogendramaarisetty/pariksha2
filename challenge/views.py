from django.shortcuts import render,redirect
from .models import Candidate,Challenge,Question,ChallengeLanguages,Language,ChallengeQuestion,CandidateChallenge,QuestionLanguageDefault,Submission,TestCase,CodeDraft
import json,requests
from .forms import CandidateForm
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404
from django.core import serializers

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
    if request.user.is_authenticated:
        user_data = get_user_data(request)
    if request.method == 'POST':
        pin = request.POST.get('pin')
        challenge = Challenge.objects.filter(pin=pin).first()
        if challenge != None:
            return redirect('candidate_details',challenge_id=str(challenge.id))
    return render(request,"home.html",{'title':'home','username':user_data['name'],'profile_pic':user_data['picture']})



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

def instructions(request,challenge_id,candidate_id):
    if request.user.is_authenticated:
        user_data = get_user_data(request)
    challenge = Challenge.objects.get(pk = challenge_id)
    candidate = Candidate.objects.filter(user = request.user).first()
    challenge_questions = ChallengeQuestion.objects.filter(challenge = challenge)
    candidate_id = str(candidate.id)
    challenge_id = str(challenge.id)
    return render(request,"instructions.html",{'title':'Instructions','challenge':challenge,'question':challenge_questions,'candidate_id':candidate_id,'challenge_id':challenge_id,'username':user_data['name'],'profile_pic':user_data['picture']})

def test_page(request,challenge_id,candidate_id):
    challenge  = Challenge.objects.get(pk = challenge_id)
    challenge_questions = ChallengeQuestion.objects.filter(challenge=challenge)   
    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST)
            res={'msg':'Code recieved success'}
            return HttpResponse(json.dumps(res), content_type="application/json")
        if request.method == 'GET':
            print(request.GET.get('qid'));
            question = Question.objects.get(pk =request.GET.get('qid') )
            res  = serializers.serialize('json', QuestionLanguageDefault.objects.filter(question = question))
            return HttpResponse(json.dumps(res), content_type="application/json")
    
    data = {
    'challenge':challenge,
    'questions':challenge_questions,
    'languages':Language.objects.all(),
    }
    return render(request,'test_page.html',data)
