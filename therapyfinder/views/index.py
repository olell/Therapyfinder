"""
Therapistfinder - therapistfinder/views/index.py

Author/s: olel
Therapistfinder (thus this code) is public domain.
"""

from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import redirect

from therapyfinder.util.user import get_user

# Create blueprint
app = Blueprint("index", "therapyfinder.views.index")


@app.route("/")
@get_user
def index(user=None):
    if user:
        return redirect(url_for("app.index"))
    return render_template("index.html")