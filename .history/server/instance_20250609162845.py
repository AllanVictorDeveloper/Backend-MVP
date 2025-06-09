from flask import Flask, Blueprint


class Server():
    def __init__(self,):
        self.app = Flask(__name__)
        self.blueprint = Blueprint('api',  __name__, url_prefix='/api')