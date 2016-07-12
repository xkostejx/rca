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
from app.mod_view.forms import SettingsForm

# Define the blueprint: 'view', set its url prefix: app.url/view
mod_view = Blueprint('view', __name__, url_prefix='/view')

from app import app

from app.mod_data.controllers import    getUserSummary, getGlobalStats, \
					getBalanceStats, getUsersDict, \
					insertDeposit, getUserByUsername, \
					forbiddenNotAdmin, forbiddenNotMeOrAdmin, \
					updateSettings, getSettings

from app.mod_data.constants import Constants as c

@app.before_request
def beforerequest():
	try:
		if 'userid' not in session or session.get('userid') is None:
			username = request.environ.get('WEBAUTH_USER')
			if username:
				user = getUserByUsername(username)
				if user:
					session.permanent = True
					session['userid'] = user.id
					session['is_logged'] = True
					session['role'] = user.role
					session['username'] = username
					session['fullname'] = user.fullname
					session['email'] = user.email
				else:
					session['role'] = -1
					session['username'] = username
					session['fullname'] = u"Neznámý uživatel"	
	except:
		abort(503)


@app.route('/', methods=['GET', 'POST'])
def index():
	return redirect(url_for('view.personalstats'))


@mod_view.route('/personal/', methods=['GET', 'POST'])
def personalstats():
	userid = session.get('userid')
	if userid:
		dusersum = json.loads(getUserSummary(userid))
		if len(dusersum):
			return render_template("personal.html", userid=userid, dusersum=dusersum[0])
		else:
			return render_template("notlogged.html")
	else:
		return render_template("notlogged.html")


@mod_view.route('/global/', methods=['GET', 'POST'])
def globalstats():
	forbiddenNotAdmin()
	dglobalstats = json.loads(getGlobalStats()).get('data')
	return render_template("global.html", dglobalstats=dglobalstats[0])


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
	
	dbalancestats = json.loads(getBalanceStats()).get('data')
	return render_template("balance.html", form=form, dbalancestats=dbalancestats[0])


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
		
		form.name.data = str(userid)
		dusersummary = getUserSummary(userid, jsonize=False)
		if len(dusersummary):
			return render_template("search.html", form=form, dusersum=dusersummary[0], userid=userid)
		else:
			return render_template("search.html", form=form, nodata=True)

	return render_template("search.html", form=form)

@mod_view.route('/settings/', methods=['GET', 'POST'])
def settings():
	forbiddenNotAdmin()
	
	form = SettingsForm(request.form)
	
	if form.validate_on_submit():
		updateSettings(form.price.data)
		flash(u"Nová cena kávy uložena.")
	else:	
		settings = getSettings()
		form.price.data = settings.price
		
	return render_template("settings.html", form=form)
