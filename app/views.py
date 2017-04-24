from flask import render_template
from app import twitteradv_app

@twitteradv_app.route('/')
@twitteradv_app.route('/index')
def index():
	return render_template('index.html')

@twitteradv_app.route('/twitter')
def twitter():
	return render_template('twitter.html')

@twitteradv_app.route('/facebook')
def facebook():
	return render_template('facebook.html')

@twitteradv_app.route('/instagram')
def instagram():
	return render_template('instagram.html')


