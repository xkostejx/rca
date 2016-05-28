# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Filter to change default datetime format
@app.template_filter()
def dateformat(value, format='%d.%m.%Y %H:%M:%S'):
    return value.strftime(format)

app.jinja_env.filters['dateformat'] = dateformat


# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_view)
from app.mod_view.controllers import mod_view as view_module

from app.mod_data.controllers import mod_data as data_module

# Register blueprint(s)
app.register_blueprint(view_module)
app.register_blueprint(data_module)

# Build the database:
# This will create the database file using SQLAlchemy

#db.create_all()
