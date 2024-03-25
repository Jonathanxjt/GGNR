from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os, sys
from os import environ
import requests
import invokes
from invokes import invoke_http
import json
app = Flask(__name__)
CORS(app)
