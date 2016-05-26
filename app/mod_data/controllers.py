# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify

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

from app import app
import json
from app.mod_data.jsonencoder import DbEncoder

@mod_data.route('/deposit/user/<userid>', methods=['GET', 'POST'])
def getdeposit(userid):
	data = db.session.query(Deposit).from_statement( \
		text("SELECT * FROM deposit WHERE user_id=:userid")).params(userid=userid).all()
	#import pdb; pdb.set_trace()
	out = [d.to_dict() for d in data]
	return json.dumps({"data" : out} )

@mod_data.route('/deposit/all', methods=['GET', 'POST'])
def getalldeposit():
	data = db.session.query(Deposit).all()
	out = [d.to_dict() for d in data]
	return json.dumps({"data" : out} )

@mod_data.route('/coffee/user/<userid>', methods=['GET', 'POST'])
def getcoffee(userid):
	data = db.session.query(Coffee).from_statement( \
		text("SELECT * FROM coffee WHERE user_id=:userid")).params(userid=userid).all()
	out = [d.to_dict() for d in data]
	return json.dumps({"data" : out} )


@mod_data.route('/coffee/user/sum', methods=['GET', 'POST'])
def getcoffeesummary():
	data = db.session.execute(text(c.SQL_COFFEE_USERS))
	out = [dict(d) for d in data]
	return json.dumps({"data" : out}, cls = DbEncoder )


@mod_data.route('/coffee/user/<userid>/sum', methods=['GET', 'POST'])
def getusersummary(userid,json = True):
	data = db.session.execute(text(c.SQL_PERSONAL_SUMMARY).params(userid=userid))
	out = [dict(d) for d in data]
	if json:
		return json.dumps(out, cls = DbEncoder )
	else:
		return out

@mod_data.route('/coffee/global/sum', methods=['GET', 'POST'])
def getglobalsummary():
        data = db.session.execute(text(c.SQL_GLOBAL_SUMMARY))
        out = [dict(d) for d in data]
        return json.dumps(out, cls = DbEncoder )

@mod_data.route('/balance/sum', methods=['GET', 'POST'])
def getbalanceummary():
        data = db.session.execute(text(c.SQL_BALANCE_SUMMARY))
        out = [dict(d) for d in data]
        return json.dumps(out, cls = DbEncoder )


def getUsersDict(surnamefirst=False):
	if surnamefirst:
		data = db.session.execute(text(c.SQL_USERS_BY_SURNAME))
	else:
		data = db.session.execute(text(c.SQL_USERS))
		
	out = [dict(d) for d in data]
	return out
