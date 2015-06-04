__author__ = 'workhorse'
from flask import Blueprint

main = Blueprint('main',__name__)

from . import views, errors #import here to avoid ciruclar dependancies


