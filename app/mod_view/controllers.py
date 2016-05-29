# coding: utf-8
import json
import logging

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort

# Import password / encryption helper tools
#from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_view.forms import LoginForm
from app.mod_view.forms import DepositForm
from app.mod_view.forms import ShowPersonForm

# Define the blueprint: 'view', set its url prefix: app.url/view
mod_view = Blueprint('view', __name__, url_prefix='/view')

from app import app

from app.mod_data.controllers import    getusersummary, getglobalsummary, \
					getbalanceummary,getUsersDict, \
					insertDeposit, getUserByUsername, \
					forbiddenNotAdmin, forbiddenNotMeOrAdmin

from app.mod_data.constants import Constants as c

@app.before_request
def beforerequest():
	try:
		if 'userid' not in session or session.get('userid') is None:
			username = request.environ.get('WEBAUTH_USER')
			if username:
				user = getUserByUsername(username)
				if user:
					session['userid'] = user.id
					session['is_logged'] = True
					session['role'] = user.role
					session['username'] = username
					session['fullname'] = user.fullname
					session['email'] = user.email
	except:
		abort(503)


@app.route('/', methods=['GET', 'POST'])
def index():
	return redirect(url_for('view.personalstats'))


@mod_view.route('/personal/', methods=['GET', 'POST'])
def personalstats():
	userid = session.get('userid')
	dusersum = json.loads(getusersummary(userid))
	return render_template("personal.html", userid=userid, dusersum=dusersum[0])


@mod_view.route('/global/', methods=['GET', 'POST'])
def globalstats():
	forbiddenNotAdmin()
	dglobalsum = json.loads(getglobalsummary())
	return render_template("global.html", dglobalsum=dglobalsum[0])


@mod_view.route('/balance/', methods=['GET', 'POST'])
def balance():
	forbiddenNotAdmin()

	form = DepositForm(request.form)
	users = getUsersDict(surnamefirst=True)
	form.name.choices = [(str(u['id']), str(u['fullnamerev'])) for u in users]

	if form.validate_on_submit():
		userid = form.name.data
		amount = form.amount.data
	        insertDeposit(userid, session['userid'], amount)
		flash(u"Vklad vložen na kávový učet.")
	
	dbalancesum = json.loads(getbalanceummary())
	return render_template("balance.html", form=form,dbalancesum=dbalancesum[0])


@mod_view.route('/search/', methods=['GET', 'POST'])
@mod_view.route('/search/user/<int:userid>', methods=['GET', 'POST'])
def search(userid = None):
	forbiddenNotAdmin()

	form = ShowPersonForm(request.form)
	users = getUsersDict(surnamefirst=True)
        form.name.choices = [(str(u['id']), str(u['fullnamerev'])) for u in users]
	
	if form.validate_on_submit() or userid:
		if not userid:
			userid = form.name.data
		
		form.name.data = userid
		dusersummary = getusersummary(userid, jsonize=False)
		return render_template("search.html", form=form, dusersum=dusersummary[0], userid=userid)

	return render_template("search.html", form=form)

