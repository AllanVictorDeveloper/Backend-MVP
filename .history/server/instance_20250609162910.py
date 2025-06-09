from flask import Flask, Blueprint
from flask_restx import Api


class Server():
    def __init__(self,):
        self.app = Flask(__name__)
        self.blueprint = Blueprint('api',  __name__, url_prefix='/api')