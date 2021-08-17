"""
Therapistfinder - therapistfinder/views/user.py

Author/s: olel
Therapistfinder (thus this code) is public domain.
"""

from flask import Blueprint
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from flask import session

from therapyfinder.models.user import User as UserModel
from therapyfinder.util.user import get_user
from therapyfinder.util.user import requires_login

# Create blueprint
app = Blueprint("user", "therapyfinder.views.user")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", None)
    if username is None:
        flash("Username is required!", "danger")
        return redirect("index.index")
    
    if UserModel.get_or_none(UserModel.name == username):
        flash("This username is already in use!", "warning")
        return redirect("index.index")

    password = request.form.get("password", None)
    if password is None:
        flash("Password is required!", "danger")

    user = UserModel.register(username, password)
    return redirect(url_for("user.login"))

@app.route("/login", methods=["GET", "POST"])
@app.route("/login/<after>", methods=["GET", "POST"])
@get_user
def login(after=None, user=None):
    if after is None:
        after = "index.index"
    
    if user is not None:
        redirect(url_for(after))

    if request.method == "GET":
        return render_template("login.html")
    
    else:
        username = request.form.get("username", None)
        if username is None:
            flash("Email is required!", "danger")
            return redirect(url_for("user.login"))
        password = request.form.get("password", None)
        if password is None:
            flash("Password is required!", "danger")
            return redirect(url_for("user.login"))
        
        user = UserModel.authenticate(username, password)
        if user is None:
            flash("Invalid username or password!", "warning")
            return redirect(url_for("user.login"))

        flash("Welcome {0}!".format(user.name), "success")
        session.update({"user_id": user.id})
        return redirect(url_for(after))

@app.route("/logout")
@requires_login
def logout(user=None, user_error=0):
    session.clear()
    return redirect(url_for("index.index"))