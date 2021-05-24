from flask import Blueprint

login_bule = Blueprint('login', __name__)
from . import views
