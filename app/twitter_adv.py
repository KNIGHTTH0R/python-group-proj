# Andrew Anderson
# ama14c

from __future__ import print_function
import tweepy
import webbrowser
import requests
from requests_oauthlib import OAuth1
import time
import sys

def print_menu():
	print("\n\n*****MENU*****")
	print("1  Get top 5 most retweeted tweets")
	print("2  Print collected tweets")
	print("3  Print tweets containing specific keyword")
	print("4  Exit")
	
def follow_followers(api, following, followers):
	snames = []
	
	for follower in followers:
		if follower not in following:
			try:
				api.create_friendship(follower)
				userobj = api.get_user(follower)
				snames.append(userobj.screen_name)
			except:
				pass
		
	return snames
	
def unfollow(api, snames):
	unfollowed = []
	for name in snames:
		try:
			userobj = api.get_user(name)
			api.destroy_friendship(userobj.id)
			unfollowed.append(userobj.screen_name)
		except:
			pass
	
	return unfollowed
	
def refollow(api, snames):
	refollowed = []
	for name in snames:
		try:
			userobj = api.get_user(name)
			api.create_friendship(userobj.id)
			refollowed.append(userobj.screen_name)
		except:
			pass
	
	return refollowed
	
def unfollow_traitors(api, following, followers):
	unfollowed = []
	for followed in following:
		if followed not in followers:
			try:
				userobj = api.get_user(followed)
				api.destroy_friendship(followed)
				unfollowed.append(userobj.screen_name)
			except:
				pass
	return unfollowed
	
def delete_tweet(api, tweets, keywrd):
	destroyed = []
	for tweet in tweets:
		if keywrd in tweet.text:
			try:
				destroyed.append(tweet)
				api.destroy_status(tweet.id_str)
			except:
				destroyed.remove(tweet)
	return destroyed

""" Unused
def get_urls(api, auth_param):
	url_list = []
	authy = OAuth1(auth_param.consumer_key, auth_param.consumer_secret, auth_param.access_token, auth_param.access_token_secret)
	statuses = tweepy.Cursor(api.user_timeline, screen_name=api.me().screen_name, include_entities=True).items()
	for status in statuses:
		url_list.append(status)
	return url_list
"""

""" Exceeds rate limit too easily
def get_most_retweets(tweets):
	most_retw_list = []
	for tweet in tweets:
		if len(most_retw_list) == 5:
			# loop through top 5 list starting from highest favorites
			for index, top in enumerate(most_retw_list):
			#retweets.count?
				if api.retweets(tweet.id) > api.retweets(top.id):
					# replace top with tweet at current index
					most_retw_list[index] = tweet
					break
		else: # add tweet to top if top 5 not filled yet
			most_retw_list.append(tweet)
"""

def get_tweets (api, num_of_tweets):
	#print('Downloading...')
	
	# add first 200 tweets (max amt) to tweetlist
	tweetlist = []
	uname = api.me().screen_name
	
	if num_of_tweets <= 200:
		templist = api.user_timeline(screen_name = uname,include_entities=True,count=num_of_tweets)
		tweetlist.extend(templist)
		#print('%d tweets downloaded' % (len(tweetlist)))
		#print('Done!')

	elif num_of_tweets > 200:
		templist = api.user_timeline(screen_name = uname,include_entities=True,count=200)
		tweetlist.extend(templist)

		# get id of last tweet to use as start of new query
		last = tweetlist[-1].id - 1
		
		# loop until indicated num of tweets downloaded
		while len(tweetlist) != num_of_tweets:
			if len(tweetlist)+200 > num_of_tweets:
				lastcount = num_of_tweets - len(tweetlist)
				time.sleep(1)
				#print('%d tweets downloaded' % (len(tweetlist)), end='\r')
				# repeat queries
				templist = api.user_timeline(screen_name = uname,include_entities=True,count=lastcount,max_id=last)
				tweetlist.extend(templist)
			
			else:
				time.sleep(1)
				#print('%d tweets downloaded' % (len(tweetlist)), end='\r')
				# repeat queries
				templist = api.user_timeline(screen_name = uname,include_entities=True,count=200,max_id=last)
				tweetlist.extend(templist)
			
			# get id of last tweet to use as start of new query
			last = tweetlist[-1].id - 1
				
		#print('%d tweets downloaded' % (len(tweetlist)))
		#print('Done!')

	return tweetlist

#Debugging:
"""
consumer_key = 'IGAHaZFkJoRieR18J1KOEvKvD'
consumer_secret = 'jf2GAPSJLf4JRm5mBEy1TbxSVrVHJZoELaZ9Ihdx4gc0ZoKyzP'
access_token = '702274436-BCmjoSQnQkvEcHgGwQ7Au6TxVLD9jLEZ6tB2tqgi'
access_token_secret = 'tNiE4XeIV8OF6fKzLhUEX7SvOydDjNeWQp2KKX1Tfj6zh'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print ('Error! Failed to get request token.')
	
webbrowser.open_new(redirect_url)
	
verifier = raw_input('Pin: ')

try:
    auth.get_access_token(verifier)
except tweepy.TweepError:
    print ('Error! Failed to get access token.')

api = tweepy.API(auth)

# get screen name of authorized user
username = api.me().screen_name

# get num of tweets to download for app use
success = False
while not success or tweets_to_DL <= 0:
	try:
		tweets_to_DL = input('\nEnter the number of tweets to download for use in this app: \n(WARNING: loading times may be long) \n(Maximum 3200): ')
		success = True
	except NameError:
		print('ERROR: invalid number entered. Try again.')
	except SyntaxError:
		print('ERROR: invalid number entered. Try again.')

#downloaded_tweets = get_tweets(username, tweets_to_DL)

for status in tweepy.Cursor(status.user_timeline, id=username, include_entities=True).items(tweets_to_DL): 
    for url in status.entities['urls']:
         print (url['expanded_url'])


print_menu()

choice = raw_input("\nEnter a menu choice: ")
while choice != "4":
	if choice == "1":
		top_retw = get_most_retweets(downloaded_tweets)
		for index, tweet in enumerate(top_retw):
			print ("# %d:" % (index+1))
			print ("Tweet: %s" % tweet.text)
			print ("Retweets: %d" % tweet.retweets.count)
			print ()
		print_menu()
		choice = raw_input("\nEnter a menu choice: ")
	elif choice == "2":
		for tweet in downloaded_tweets:
			print ("Tweet: %s" % tweet.text)
			print ("Date: %s" % tweet.created_at)
			print ('\n')
		print_menu()
		choice = raw_input("\nEnter a menu choice: ")
	elif choice == "3":
		mention_choice = raw_input("\nEnter a user to search for: ")
		print()
		for tweet in downloaded_tweets:
			if mention_choice in tweet.text:
				print ("Tweet: %s" % tweet.text)
				print ("Date: %s" % tweet.created_at)
				print ('\n')
		print_menu()
		choice = raw_input("\nEnter a menu choice: ")
	else:
		print('Invalid, try again: ')
		choice = raw_input("\nEnter a menu choice: ")
"""
	

