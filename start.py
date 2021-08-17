"""
Therapistfinder - start.py

Author/s: olel
Therapistfinder (thus this code) is public domain.
"""

## Creating flask app
from flask import Flask
from flask.helpers import url_for
app = Flask(__name__)

app.secret_key = "slkdnfmwioqf3n9203nfkldfnv" ## Todo config

# Blueprints
from therapyfinder.views.index import app as index_view_blueprint
from therapyfinder.views.user import app as user_view_blueprint
from therapyfinder.views.app import app as app_view_blueprint
app.register_blueprint(index_view_blueprint)
app.register_blueprint(user_view_blueprint, url_prefix="/user")
app.register_blueprint(app_view_blueprint, url_prefix="/app")

# Global imports

# Local imports
from therapyfinder.util.user import get_user_object

# Some jinja addons
@app.context_processor
def inject_templates():
    user_obj = get_user_object()
    return {
        "user": user_obj,
    }