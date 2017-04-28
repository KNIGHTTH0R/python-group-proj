from flask import Flask, render_template, session, request, redirect, abort, flash, jsonify, url_for
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
from instagram.client import InstagramAPI
import flask
import requests
import tweepy
from app.twitter_adv import get_tweets, delete_tweet, unfollow_traitors, follow_followers, unfollow, refollow
from app import t_app

# for instagram
t_app.secret_key = 'super secret key'
ig_credentials = {
    'client_id': "fcf2484c92244827b3bcc23d39a61b16",
    'client_secret': "086878ff36a148f4aca782c5bc145f99",
    'redirect_uri': "http://localhost:5000/instagram_callback"
}
api = InstagramAPI(**ig_credentials)

# for twitter
consumer_key = 'IGAHaZFkJoRieR18J1KOEvKvD'
consumer_secret = 'jf2GAPSJLf4JRm5mBEy1TbxSVrVHJZoELaZ9Ihdx4gc0ZoKyzP'
callback_url = 'http://127.0.0.1:5000/twitter_verify'

session = dict()
access_info = dict() # to store access info once obtained
tweetlist = []
tweets_to_DL = None

auth = None
names = None

@t_app.route('/')
@t_app.route('/index')
def index():
	return render_template('index.html')
	
########################################
###  Twitter Section
###
#######################################
	
@t_app.route('/twitter_redir')
def send_token():
	global auth
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

	try:
		redirect_url = auth.get_authorization_url()
		session['request_token'] = auth.request_token
	except tweepy.TweepError:
		print ('Error! Failed to get request token.')
		
	return redirect(redirect_url)

# callback. once twitter authorizes user, it sends user back to this page
@t_app.route('/twitter_verify')
def get_verification():
	global auth
	#get the verifier key from the request url
	verifier = request.args['oauth_verifier']

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	token = session['request_token']
	del session['request_token']

	auth.request_token = token
	
	try:
		auth.get_access_token(verifier)
	except tweepy.TweepError:
		print 'Error! Failed to get access token.'
		
	api = tweepy.API(auth)
	# cache info to avoid rate limit
	access_info['api'] = api
	access_info['following'] = api.friends_ids(api.me().screen_name)
	access_info['followers'] = api.followers_ids(api.me().screen_name)
	access_info["access_token"] = auth.access_token
	access_info["access_token_secret"] = auth.access_token_secret
	
		
	return redirect(url_for('twitter_DL'))
	
@t_app.route('/twitter_DL', methods=['GET', 'POST'])
def twitter_DL():
	global tweetlist
	global tweets_to_DL
	# redirect to twitter sign in page if not done yet
	if 'access_token' in access_info:
		if request.method == 'POST':
			tweets_to_DL = request.form['tweet_count']
		else:
			tweets_to_DL = None
		if tweets_to_DL is None:
			return render_template('twitter_DL.html')
		elif int(tweets_to_DL) <= 0 or int(tweets_to_DL) > 3200:
			return render_template('twitter_DL.html')
		else:
			tweetlist = get_tweets(access_info['api'], int(tweets_to_DL))
			return redirect(url_for('twitter'))
	else:
		return redirect(url_for('send_token'))
	
@t_app.route('/twitter')
def twitter():
	# redirect to twitter sign in page if not done yet
	if 'access_token' in access_info:
		return render_template('twitter.html')
	else:
		return redirect(url_for('send_token'))

	
@t_app.route('/twitter/twitter_feat1', methods=['GET', 'POST'])
def twitter_feat1():
	#Follow back all followers
	global auth
	global names
	arguments = []
	# redirect to twitter sign in page if not done yet
	if 'access_token' in access_info:
		if request.method == 'POST':
			"""
			for f in request.form:
				arguments.append(f)
			return render_template('twitter_feat1.html', arguments=f)
			"""
			if 'u' in request.form:
				unfollowed = unfollow(access_info['api'], names)
				return render_template('twitter_feat1.html', unfollowed=unfollowed)
			else:
				names = follow_followers(access_info['api'], access_info['following'], access_info['followers'])
				return render_template('twitter_feat1.html', names=names)
		else:
			return render_template('twitter_feat1.html')
	else:
		return redirect(url_for('send_token'))

@t_app.route('/twitter/twitter_feat2', methods=['GET', 'POST'])
def twitter_feat2():
	#Unfollow users who don't follow you back
	global auth
	global names
	# redirect to twitter sign in page if not done yet
	if 'access_token' in access_info:
		if request.method == 'POST':
			if 'u' in request.form:
				refollowed = refollow(access_info['api'], names)
				return render_template('twitter_feat2.html', refollowed=refollowed)
			else:
				names = unfollow_traitors(access_info['api'], access_info['following'], access_info['followers'])
				return render_template('twitter_feat2.html', names=names)
		else:
			return render_template('twitter_feat2.html')
	else:
		return redirect(url_for('send_token'))	
	
@t_app.route('/twitter/twitter_feat3', methods=['GET', 'POST'])
def twitter_feat3():
	#Find tweets containing specific keyword
	global auth
	# redirect to twitter sign in page if not done yet
	if 'access_token' in access_info:
		if request.method == 'POST':
			search_key = request.form['search_key']
			return render_template('twitter_feat3.html', tweets=tweetlist, search_key=search_key)
		else:
			return render_template('twitter_feat3.html')
	else:
		return redirect(url_for('send_token'))
		
@t_app.route('/twitter/twitter_feat4', methods=['GET', 'POST'])
def twitter_feat4():
	#View tweets from specific date
	global auth
	global tweetlist
	# redirect to twitter sign in page if not done yet
	if 'access_token' in access_info:
		if request.method == 'POST':
			search_key = str(request.form['search_key'])
			return render_template('twitter_feat4.html', tweets=tweetlist, search_key=search_key)
		else:
			return render_template('twitter_feat4.html')
	else:
		return redirect(url_for('send_token'))
		
@t_app.route('/twitter/twitter_feat5', methods=['GET', 'POST'])
def twitter_feat5():
	#Delete tweets with specific keyword
	global auth
	# redirect to twitter sign in page if not done yet
	if 'access_token' in access_info:
		if request.method == 'POST':
			search_key = request.form['search_key']
			destroyed = delete_tweet(access_info['api'], tweetlist, search_key)
			return render_template('twitter_feat5.html', destroyed=destroyed, keywrd=search_key)
		else:
			return render_template('twitter_feat5.html')
	else:
		return redirect(url_for('send_token'))

########################################
###  Facebook Section
###
#######################################
		
@t_app.route('/facebook')
def facebook():
	return render_template('facebook.html')
	
########################################
###  Instagram Section
###
#######################################

@t_app.route('/instagram')
def user_photos():
	#check for IG info in session variables
	if 'instagram_access_token' in session and 'instagram_user' in session:
		userAPI = InstagramAPI(access_token=session['instagram_access_token'])
		recent_media, next=userAPI.user_recent_media(user_id=session['instagram_user'].get('id'),count=10)

		template_data = {
			'size' : request.args.get('size', 'thumb'),
			'media' : recent_media
		}

		return render_template('layout.html', **template_data)

	else:
		return redirect('/ig_connect')

@t_app.route('/ig_connect')
def main():
	url = api.get_authorize_url(scope=["likes", "comments"])
	return redirect(url)

@t_app.route('/instagram_callback')
def instagram_callback():

	code = request.args.get('code')

	if code:
		access_token, user = api.exchange_code_for_access_token(code)
		if not access_token:
			return 'Could not get access token'

		t_app.logger.debug('got an access token')
		t_app.logger.debug(access_token)

		# Sessions are used to keep this data
		session['instagram_access_token'] = access_token
		session['instagram_user'] = user

		return redirect('/instagram') # redirect back to main page

	else:
		return "Uhoh no code provided"

@t_app.route('/instagram/mostliked')
def most_liked_photo():
	if 'instagram_access_token' in session and 'instagram_user' in session:
		userAPI = InstagramAPI(access_token=session['instagram_access_token'])
		recent_media, next=userAPI.media_popular(user_id=session['instagram_user'].get('id'),count=10)

		template_data = {
			'size' : request.args.get('size', 'thumb'),
			'media' : recent_media
		}

		return render_template('layout.html', **template_data)

	else:
		return redirect('/ig_connect')


