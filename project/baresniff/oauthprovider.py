from datetime import datetime, timedelta
from flask import request, render_template, g
from baresniff import db, app, oauth, web_content
from forms import ResourceOwnerAuthorizeForm
from baresniff.models import Client, Grant, Token, User
from flask.ext.login import login_user, logout_user, current_user, login_required

from pprint import pprint

@oauth.clientgetter
def load_client(client_id):
    return Client.objects(id=client_id).first() #TODO: Exception handling.

@oauth.grantgetter
def load_grant(client_id, code):
    app.logger.debug("Inside load_grant with client_id:{client_id} and code:{code}".format(
        client_id=client_id, code=code))
    client = Client.objects(id=client_id).first()
    return Grant.objects(client=client, code=code).first()
    
@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    #TODO: Place the expires time in the settings
    expires = datetime.utcnow() + timedelta(seconds=8640000)
    app.logger.debug("Inside save_grant with client_id: {client_id}".format(client_id=client_id))
    client = Client.objects(id=client_id).first() #TODO: Exception handling
    user = User.objects(id=g.user.id).first()
    app.logger.debug("User-id:{user_id}".format(user_id=g.user.id))
    grant = Grant(
        client=client,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        scopes=request.scopes, #documentation for SQLAlchemy says _scopes=''.join(request.scopes) #confirm
        user=user, #get_current_user()
        expires=expires
    )
    grant.save()
    return grant
    
@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.objects(access_token=access_token).first()
    elif refresh_token:
        return Token.objects(refresh_token=refresh_token).first()

@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    client = Client.objects(id=request.client.id).first()
    user = User.objects(id=request.user.id).first()
    toks = Token.objects(client=client,
        user=user)
    #Making sure that every client has only one token connected to a user
    toks.delete()
    
    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)
    
    tok = Token(**token)
    tok.expires = expires
    tok.client = client
    tok.user = user
    tok.scopes = request.scopes
    tok.save()
    return tok
@app.route('/oauth/test')
def test_url_for_oauth(*args, **kwargs):
    return "test success"
    
@app.route('/oauth/authorize', methods=['GET', 'POST'])
@login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    form = ResourceOwnerAuthorizeForm()
    if not form.validate_on_submit():
        pprint (form.errors)
    if form.validate_on_submit():
#    if request.method == 'POST':
        app.logger.debug("Inside POST block of authorize. validate_on_submit is true")
        confirm = request.form.get('confirm', 'no')
        app.logger.debug("Confirm:{confirm}".format(confirm=confirm))
        #TODO: Let resource owner select scopes. Change oauthorize.html/ResourceOwnerAuthorizeForm
        #request.scopes = 'email'
        #request.__setitem__('scopes', 'email')
        app.logger.debug("Client_id:{client_id}".format(client_id=request.args.get('client_id')))
#        request.client = Client.objects(id=
        return True #confirm == 'yes'
    app.logger.debug("Inside get block of authorize")
    #available only on GET
    client_id = request.args.get('client_id') #kwargs.get('client_id')
    app.logger.debug("Client-id:{client_id}".format(client_id=client_id))
    pprint (kwargs.get('scopes'))
    client = Client.objects(id=client_id).first()
    kwargs['client'] = client
    kwargs['form'] = form
    return render_template('oauthorize.html', 
        web_content_ui=web_content.ui_elements,
        user=g.user,
#         client=client,
#         form=form)
        **kwargs)
        
        ##The parameters in **kwargs:
        #	client_id: id of the client
        #	scopes: a list of scope
        #	state: state parameter
        #   redirect_uri: redirect_uri parameter
        #	response_type: response_type parameter
        
#     confirm = request.form.get('confirm', 'no')
#     app.logger.debug("Confirm:{confirm}".format(confirm=confirm))
#     return confirm == 'yes'
    
@app.route('/oauth/token') #To limit to post-only for exchange tokens add methods=['POST']
@oauth.token_handler
def access_token():
    app.logger.debug("Inside oauth/token")
    return None #add more data like -> return {'version': '0.0.1'}
    
