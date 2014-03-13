#resource file 
from baresniff import app, login_manager, oauth, bs_environment
from baresniff.models import User, Sniff, Comment, BaseSniff, Client

from flask import abort
from flask.ext.login import login_user, logout_user, current_user, login_required
#REST imports
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.authentication import AuthenticationBase
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods
from pprint import pprint

api = MongoRest(app)

class ApiKeyAuthentication(AuthenticationBase):
    def authorized(self):
        @oauth.require_oauth('email')
        def oauth_dummy_fun(data):
            return "data"
        if oauth_dummy_fun():
            return True
        else:
            return False

class BaseResourceView(ResourceView):
    if bs_environment is not "test_without_oauth":
        authentication_methods = [ApiKeyAuthentication]
    
class UserResource(Resource):
    document = User
    
    filters = {
        'username': [ops.Exact,]
    }
        
class CommentResource(Resource):
    document = Comment

class SniffResource(Resource):
    document = Sniff
    related_resources = {
        'comments': CommentResource,
    }
    filters = {
        'title': [ops.Exact,] #, ops.StartsWith],
    }
    
class BaseSniffResource(Resource):
    document = BaseSniff
    related_resources = {
        'user': UserResource,
    }

class ClientResource(Resource):
    document = Client
    
#TODO: To add comments the api currently expects the whole object (as JSON) with the new 
#  comments appended to it. Need to change this behavior and find the best practices for doing this.

#TODO: Include a uri field for reference objects

#TODO: Give an end point to show only number-of-comments with each post and not the entire comments.
@api.register(name='sniffs', url='/sniff/')
class SniffView(BaseResourceView):
    resource = SniffResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]
    
@api.register(name='basesniff', url='/basesniff/')
class BaseSniffView(BaseResourceView):
    resource = BaseSniffResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

@api.register(name='users', url='/user/')
class UserView(BaseResourceView):
    resource = UserResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]
    
@api.register(name='client', url='/client/')
class ClientView(BaseResourceView):
    resource = ClientResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]
