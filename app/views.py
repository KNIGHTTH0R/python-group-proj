from flask import render_template
from app import t_app

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
