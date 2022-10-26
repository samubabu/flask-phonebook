from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] ='U-IL-NVR-GZ'

from . import routes