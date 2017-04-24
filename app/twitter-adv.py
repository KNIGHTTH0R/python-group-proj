# Andrew Anderson
# ama14c

from __future__ import print_function
import tweepy
import webbrowser
import time
import sys

""" TODO
-option at beginning to download certain number of tweets

"""

def print_menu():
	print("\n\n*****MENU*****")
	print("1  Get top 5 most retweeted tweets")
	print("2  Print collected tweets")
	print("3  Print tweets mentioning specific user")
	print("4  Exit")

def get_most_retweets(tweets):
	most_retw_list = []
	for tweet in tweets:
		if len(most_retw_list) == 5:
			# loop through top 5 list starting from highest favorites
			for index, top in enumerate(most_retw_list):
				if api.retweets(tweet.id) > api.retweets(top.id):
					# replace top with tweet at current index
					most_retw_list[index] = tweet
					break
		else: # add tweet to top if top 5 not filled yet
			most_retw_list.append(tweet)
	

def get_tweets (uname, num_of_tweets):
	print('Downloading...')

	# add first 200 tweets (max amt) to tweetlist
	tweetlist = []
	
	
	if num_of_tweets <= 200:
		templist = api.user_timeline(screen_name = uname,count=num_of_tweets)
		tweetlist.extend(templist)
		print('%d tweets downloaded' % (len(tweetlist)))
		print('Done!')

	elif num_of_tweets > 200:
		templist = api.user_timeline(screen_name = uname,count=200)
		tweetlist.extend(templist)

		# get id of last tweet to use as start of new query
		last = tweetlist[-1].id - 1
		
		# loop until indicated num of tweets downloaded
		while len(tweetlist) != num_of_tweets:
			if len(tweetlist)+200 > num_of_tweets:
				lastcount = num_of_tweets - len(tweetlist)
				time.sleep(1)
				print('%d tweets downloaded' % (len(tweetlist)), end='\r')
				sys.stdout.flush()
				# repeat queries
				templist = api.user_timeline(screen_name = uname,count=lastcount,max_id=last)
				tweetlist.extend(templist)
			
			else:
				time.sleep(1)
				print('%d tweets downloaded' % (len(tweetlist)), end='\r')
				sys.stdout.flush()
				# repeat queries
				templist = api.user_timeline(screen_name = uname,count=200,max_id=last)
				tweetlist.extend(templist)
			
			# get id of last tweet to use as start of new query
			last = tweetlist[-1].id - 1
				
		print('%d tweets downloaded' % (len(tweetlist)))
		print('Done!')

	return tweetlist

consumer_key = 'IGAHaZFkJoRieR18J1KOEvKvD'
consumer_secret = 'jf2GAPSJLf4JRm5mBEy1TbxSVrVHJZoELaZ9Ihdx4gc0ZoKyzP'
access_token = '702274436-BCmjoSQnQkvEcHgGwQ7Au6TxVLD9jLEZ6tB2tqgi'
access_token_secret = 'tNiE4XeIV8OF6fKzLhUEX7SvOydDjNeWQp2KKX1Tfj6zh'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

"""
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
"""

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

downloaded_tweets = get_tweets(username, tweets_to_DL)

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
	

