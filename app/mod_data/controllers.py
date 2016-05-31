# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, \
		  jsonify, abort

from sqlalchemy import text,desc

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.mod_data.models import User
from app.mod_data.models import Deposit
from app.mod_data.models import Coffee 

# Import contants
from app.mod_data.constants import Constants as c

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_data = Blueprint('data', __name__, url_prefix='/data')

import json
from app import app
from app.mod_data.jsonfactory import DbEncoder, data2json as d2j

@mod_data.route('/deposit/user/<int:userid>', methods=['GET', 'POST'])
def getDepositByUser(userid):
	forbiddenNotMeOrAdmin(userid)

	data = db.session.execute(text(c.SQL_USER_DEPOSIT).params(userid=userid))
	return d2j.fromDB(data)

@mod_data.route('/deposit/user/all', methods=['GET', 'POST'])
def getDepositAll():
	forbiddenNotAdmin()
	
	data = db.session.execute(text(c.SQL_DEPOSIT))
	return d2j.fromDB(data)

@mod_data.route('/deposit/delete/<int:depositid>', methods=['GET', 'POST'])
def deleteDepositById(depositid):
	forbiddenNotAdmin()

	Deposit.query.filter_by(id=depositid).delete()
	db.session.commit()
	return redirect(url_for('view.balance'))


@mod_data.route('/coffee/user/<int:userid>', methods=['GET', 'POST'])
def getCoffeeByUser(userid):
	forbiddenNotMeOrAdmin(userid)
	data = Coffee.query.filter_by(user_id=userid).order_by(desc("date_created")).limit(100)
	
	return d2j.fromDB(data, True)

@mod_data.route('/coffee/user/sum', methods=['GET', 'POST'])
def getCoffeeSummary():
	forbiddenNotAdmin()

	data = db.session.execute(text(c.SQL_COFFEE_SUMMARY))
	return d2j.fromDB(data)

@mod_data.route('/coffee/user/sum/<int:userid>', methods=['GET', 'POST'])
def getUserSummary(userid,jsonize = True):
	forbiddenNotMeOrAdmin(userid)

	data = db.session.execute(text(c.SQL_USER_SUMMARY).params(userid=userid))
	out = [dict(d) for d in data]
	if jsonize:
		return json.dumps(out, cls = DbEncoder )
	else:
		return out

@mod_data.route('/coffee/global/stats', methods=['GET', 'POST'])
def getGlobalStats():
	forbiddenNotAdmin()

        data = db.session.execute(text(c.SQL_GLOBAL_STATS))
	return d2j.fromDB(data)

@mod_data.route('/coffee/balance/stats', methods=['GET', 'POST'])
def getBalanceStats():
	forbiddenNotAdmin()

        data = db.session.execute(text(c.SQL_BALANCE_STATS))
	return d2j.fromDB(data)

def getUsersDict(surnamefirst=False):
	if surnamefirst:
		data = db.session.execute(text(c.SQL_USERS_REV))
	else:
		data = db.session.execute(text(c.SQL_USERS))
		
	out = [dict(d) for d in data]
	return out

def getUserByUsername(username):
	return User.query.filter_by(username=username).first()	

def insertDeposit(userid, adminid, amount):
	db.session.add(Deposit(userid, adminid, amount))
	db.session.commit()

def forbiddenNotAdmin():
        if session.get('role') != c.ROLE_ADMIN:
                abort(403)

def forbiddenNotMeOrAdmin(userid):
        if session.get('userid') != userid and session.get('role') != c.ROLE_ADMIN:
                abort(403)
