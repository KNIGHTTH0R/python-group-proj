#Jared Kraemer
#jgk14

from __future__ import print_function
import facebook
import requests
import json


'''access token from app'''
app_id = '980933068710567'
app_secret = 'q-NDs4zOcM9Ak7nTohpNaiKhqCI'
access_token = app_id + "|" + app_secret


def getFriends():	
	''' print out friends list'''
	graph = facebook.GraphAPI(access_token)
	profile = graph.get_object("me")
	friends = graph.get_connections("me", "friends")

	friend_list = [friend['name'] for friend in friends['data']]

	print(friend_list)

def attemptConnect(url):
	
	while True:
		response = requests.get(url)
		'''
		if response is not Error:
			break
		try:
			jsonDict = (response.text)
		except ValueError:
			break
		'''
	return response
	
def getComments(id = None):
	graph = facebook.GraphAPI(access_token)
	
	one = "https://graph.facebook.com/v2.6"
	two = "/me" if id is None else id
	three = "/comments"
	four = "?fields=id,like_count,comments"
	five = "&order=chronological&limit=10&access_token=" + access_token
	url = one + two + three + four + five
	
	response = attemptConnect(url)
	
	return json.loads(response)
	
def main():
	'''load all comments and sort by likes'''
	comments = getComments("me")
	next = True
	while next and comments is not None:
		#getComments(access_token, comment['id'])
		if 'paging' in comments:		
			if 'next' in comments['paging']:
				res = getComments(comments['paging']['next'])
				comments = json.loads(res)
			else:
				next = False