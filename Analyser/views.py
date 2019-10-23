from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from . import forms
from django.contrib.auth.decorators import login_required

import string
import re
from textblob import TextBlob
import tweepy
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize


def preprocess_tweet(text):

    # Check characters to see if they are in punctuation
    nopunc = [char for char in text if char not in string.punctuation]
    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    # convert text to lower-case
    nopunc = nopunc.lower()
    # remove URLs
    nopunc = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', nopunc)
    nopunc = re.sub(r'http\S+', '', nopunc)
    # remove usernames
    nopunc = re.sub('@[^\s]+', '', nopunc)
    # remove the # in #hashtag
    nopunc = re.sub(r'#([^\s]+)', r'\1', nopunc)
    # remove repeated characters
    nopunc = word_tokenize(nopunc)
    # remove stopwords from final word list
    return [word for word in nopunc if word not in stopwords.words('english')]

def tostring(tweet):
    x=''
    for i in tweet:
        x=x+i
        x=x+' '
    return(x)

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
def classifyTweet(tweet_polarity):
	if tweet_polarity <=0.05:
		return "Negative"
	elif tweet_polarity > 0.05 and tweet_polarity < 0.12:
		return "Neutral"
	else:
		return "Positive"

@login_required(login_url="/Accounts/login/")
def analyseTweets(request,hashtag):
	# accept the tweet as an input here and then apply ml on it and send a list of context with the results.
	tweet = hashtag
	consumer_key = "Qqu3s8I0OWEpxC4cbbCC2Bh8D" 
	consumer_secret = "wBbdhFIm7o9HIu7qywlpvPGiHgeeEPezhMzQyeTlNB2NEVPUWc"
	access_key = "2464758009-fvdSfd6YNtlzmFTHKRlOtBypps0R6rx9NKyxKMs"
	access_secret = "CaX9VIccghKGvKnhyXdSscJEWWX0Hln7tg7xRt6bdV5fv"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	public_tweets = api.search(tweet, lang='en')
    # print("number of tweets extracted: " + str(len(public_tweets)))
    # print(len(public_tweets))
	polarityIndividual = {}
	if len(public_tweets)!=0:
		total_polarity=0
		for tweet in public_tweets:
            #print(tweet.text)
			currentTweet = tweet.text
			good_tweet=preprocess_tweet(tweet.text)
            #print(good_tweet)
			tweet_string=tostring(good_tweet)
            # print(tweet_string)
			analysis = TextBlob(tweet_string)
            # print(analysis.sentiment.polarity)
			polarityIndividual[currentTweet] = classifyTweet(analysis.sentiment.polarity)
			total_polarity=total_polarity+analysis.sentiment.polarity
            # print("\n")
			tweet_polarity=total_polarity/len(public_tweets)
		if tweet_polarity <=0.05:
			polarityResult = "Negative"
		elif tweet_polarity > 0.05 and tweet_polarity < 0.12:
			polarityResult = "Neutral"
		else:
			polarityResult = "Positive"
		print(polarityIndividual)
	else:
		polarityResult = "No tweets found for this search"
		tweet_polarity = None
		polarityIndividual["No tweet"] = "No tweet"
	return render(request,'Analyser/showTweets.html', 
							{
								'hashtag':hashtag,
								'polarityResult' : polarityResult,
								'tweet_polarity' : tweet_polarity,
								'polarityIndividual' : polarityIndividual
							})

@login_required(login_url="/Accounts/login/")
def showTweets(request):
	return render(request,'Analyser/showTweets.html')