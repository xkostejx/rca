# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
#from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_view.forms import LoginForm
from app.mod_view.forms import DepositForm
from app.mod_view.forms import ShowPersonForm

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_view = Blueprint('view', __name__, url_prefix='/view')

from app import app

from app.mod_data.controllers import getusersummary, getglobalsummary,getbalanceummary,getUsersDict

import json


@app.route('/', methods=['GET', 'POST'])
def index():
	return redirect(url_for('view.personalstats'))


@mod_view.route('/personal/', methods=['GET', 'POST'])
def personalstats():
	dusersum = json.loads(getusersummary(2))
	return render_template("personal.html",dusersum=dusersum[0])

@mod_view.route('/global/', methods=['GET', 'POST'])
def globalstats():
	dglobalsum = json.loads(getglobalsummary())
	return render_template("global.html", dglobalsum=dglobalsum[0])

@mod_view.route('/balance/', methods=['GET', 'POST'])
def balance():
	dbalancesum = json.loads(getbalanceummary())
	form = DepositForm(request.form)
	users = getUsersDict(surnamefirst=True)
	form.name.choices = [(str(u['id']), str(u['fullnamerev'])) for u in users]

	if form.validate_on_submit():
		name = form.name.data
		amount = form.amount.data
		flash("Deposit successfuly added.")
	
	return render_template("balance.html", form=form,dbalancesum=dbalancesum[0])


@mod_view.route('/search/', methods=['GET', 'POST'])
def search():
	form = ShowPersonForm(request.form)
	users = getUsersDict(surnamefirst=True)
        form.name.choices = [(str(u['id']), str(u['fullnamerev'])) for u in users]
	
	if form.validate_on_submit():
		userid = form.name.data
		dusersummary = getusersummary(userid, jsonize=False)
		#import pdb; pdb.set_trace()
		return render_template("search.html", form=form, dusersum=dusersummary[0], userid=userid)

	return render_template("search.html", form=form)

