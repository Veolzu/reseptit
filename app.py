from flask import Flask
from flask import abort, make_response, redirect, render_template, request, session
import config, users

app = Flask(__name__)
app.secret_key = config.secret_key
