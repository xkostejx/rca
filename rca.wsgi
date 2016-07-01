import os
import sys
import site

# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__), 'local/lib/python2.7/site-packages'))

# Path of execution
sys.path.append('/opt/rca')

# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))

# import rca app as application
from app import app as application
