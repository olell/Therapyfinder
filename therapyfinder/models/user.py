"""
Therapistfinder - therapistfinder/models/user.py

Author/s: olel
Therapistfinder (thus this code) is public domain.
"""

# Global imports
import peewee
from argon2 import PasswordHasher

# Local imports
from therapyfinder.models import Database

class User(peewee.Model):

    # Basic account information
    name = peewee.CharField(max_length=50)
    password = peewee.CharField(default="")

    def set_password(self, plain_text_password):
        ph = PasswordHasher()
        self.password = ph.hash(plain_text_password)

    def check_password(self, plain_text_password):
        ph = PasswordHasher()
        try:
            return ph.verify(self.password, plain_text_password)
        except:
            return False

    @staticmethod
    def register(username, plain_text_password):
        user = User(
            name=username
        )
        user.set_password(plain_text_password)
        user.save()
        return user
        
    @staticmethod
    def authenticate(username, password):
        user = User.get_or_none(User.name == username)
        if user is not None:
            if user.check_password(password):
                return user
        return None

    
    class Meta:
        database = Database.get()

Database.register_models(User)