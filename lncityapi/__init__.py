
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from lncityapi.other.common import db, db_connect_string

# Initialize app

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = db_connect_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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
import lncityapi.api.tags
import lncityapi.api.pokers
