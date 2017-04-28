from flask import Flask, render_template, session, request, redirect, abort, flash, jsonify
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
from instagram.client import InstagramAPI
from app import t_app


t_app.secret_key = 'super secret key'
ig_credentials = {
    'client_id': "fcf2484c92244827b3bcc23d39a61b16",
    'client_secret': "086878ff36a148f4aca782c5bc145f99",
    'redirect_uri': "http://localhost:5000/instagram_callback"
}
api = InstagramAPI(**ig_credentials)


@t_app.route('/')
@t_app.route('/index')
def index():
	return render_template('index.html')

@t_app.route('/twitter')
def twitter():
	return render_template('twitter.html')

@t_app.route('/facebook')
def facebook():
	return render_template('facebook.html')

########################################
###  Instagram Section1
###
#######################################

@t_app.route('/instagram')
def user_photos():
	#check for IG info in session variables
	if 'instagram_access_token' in session and 'instagram_user' in session:
		userAPI = InstagramAPI(access_token=session['instagram_access_token'])
		recent_media, next=userAPI.user_recent_media(user_id=session['instagram_user'].get('id'),count=20)

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

# @t_app.route('/instagram/mostliked')
# def most_liked_photo():


########################################
###  End Instagram Section
###
#######################################

# @t_app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404
