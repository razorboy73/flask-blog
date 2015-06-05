__author__ = 'workhorse'
from flask import Blueprint

auth = Blueprint('auth', __name__)
#could also use template_folder='templates' - would route things to a seperate template file
from . import views
#imported below to avoid circular references

