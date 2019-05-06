
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
import lncityapi.api.users
import lncityapi.api.balances
import lncityapi.api.slots
import lncityapi.api.blogs
import lncityapi.api.roulettes
import lncityapi.api.tips
import lncityapi.api.notifications
