from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from . import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/Accounts/login/")
def home(request):
	if request.method == 'POST':
	     form = forms.HashtagForm(request.POST)
	     if form.is_valid():
	         instance = form.save(commit=False)
	         print(instance.Hashtag_Searched)
	         hashtag = instance.Hashtag_Searched
	         instance.Username = request.user
	         print(instance.Username)
	         instance.save()
	         return analyseTweets(request,hashtag)
	else:
		form = forms.HashtagForm()
	return render(request, 'Analyser/home.html', { 'form': form })

@login_required(login_url="/Accounts/login/")
def analyseTweets(request,hashtag):
	# accept the tweet as an input here and then apply ml on it and send a list of context with the results.
	tweet = hashtag
	return render(request,'Analyser/showTweets.html', {'tweet':tweet})

@login_required(login_url="/Accounts/login/")
def showTweets(request):
	return render(request,'Analyser/showTweets.html')