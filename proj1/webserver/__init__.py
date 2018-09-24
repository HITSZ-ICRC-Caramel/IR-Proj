__author__ = 'lzj'

from flask import Flask
import sys
sys.path.append("..")

app = Flask(__name__)
from webserver import views

