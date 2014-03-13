import datetime
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_login import LoginManager
#from flask_oauthlib.provider import OAuth1Provider
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)

#TODO: Move to a separate configuration file
app.debug = True
app.config["MONGODB_SETTINGS"] = {'DB': "bs_fox_test_03"}
app.config["SECRET_KEY"] = "\x8al\x18\xb3\x92[Z\x1a+\xc5(" #os.urandom(15)

app.config["OAUTH2_PROVIDER_TOKEN_EXPIRES_IN"] = 8650000

db = MongoEngine(app)
#oauth1 = OAuth1Provider(app)
oauth2 = OAuth2Provider(app)
oauth = oauth2
login_manager = LoginManager(app)

bs_environment = "test_with_oauth" #"test_without_oauth"

from baresniff import models, views, resources, oauthprovider

if __name__ == '__main__':
    app.run()
