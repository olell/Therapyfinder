"""
Therapistfinder - therapistfinder/util/user.py

Author/s: olel
Therapistfinder (thus this code) is public domain.
"""

# Global imports
from functools import wraps
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

# Local imports
from therapyfinder.models.user import User

def requires_login(endpoint):
    """
    user_errors:
    0 -> Logged in
    1 -> Not logged in
    :param endpoint:
    :return:
    """

    @wraps(endpoint)
    def check_login(*args, **kwargs):
        user_id = session.get("user_id", None)
        if user_id is not None:
            user = User.get(User.id == user_id)
            if user is not None:
                kwargs.update({"user": user, "user_error": 0})
                return endpoint(*args, **kwargs)
        
        flash("The requested page requires that your logged in :)")
        return redirect(url_for("user.login", after=request.endpoint))

    return check_login


def get_user(endpoint):
    @wraps(endpoint)
    def check_login(*args, **kwargs):
        user_id = session.get("user_id", None)
        if user_id is not None:
            user = User.get_or_none(User.id == user_id)
            if user is not None:
                kwargs.update({"user": user})
                return endpoint(*args, **kwargs)
        kwargs.update({"user": None})
        return endpoint(*args, **kwargs)

    return check_login

def get_user_object():
    user_id = session.get("user_id", None)
    if user_id is not None:
        user = User.get_or_none(User.id == user_id)
        return user
    return None
