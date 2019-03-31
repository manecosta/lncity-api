
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

# Initialize app

app = Flask(__name__)
CORS(app)

loginManager = LoginManager()
loginManager.init_app(app)

# Import api files

import lncityapi.api.invoices
