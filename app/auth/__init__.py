from flask import Blueprint

#create instance of Blueprint to rep the authentication blueprint

auth_blueprint=Blueprint('auth',__name__)

from . import views