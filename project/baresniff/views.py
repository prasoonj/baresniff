#Stores the views for the app
import os
from util import random_id_generator
from flask import render_template, flash, redirect, request, g, url_for, session
from baresniff import app, login_manager, models, oauth, db, web_content, fields as custom_fields
from forms import LoginForm, ClientRegistrationForm, UserRegistrationForm
from flask.ext.login import login_user, logout_user, current_user, login_required
import json
from pprint import pprint

###LoginManager customizations### TODO: Move to global config file
login_manager.login_view = "login"
login_manager.login_message = u"Please login to access this page."
login_manager.login_message_category = "info"
login_manager.session_protection = "strong" #basic or None are available 

@app.before_request
def before_reqeust():
    g.user = current_user
    pprint (request.headers)
#     pprint (request.get_json()['user_id'])
    if current_user.is_anonymous() == True:
        app.logger.debug("Inside before_request with anonymous: %s !\n" % current_user.get_id())
    else:
        app.logger.debug("Inside before_request with current_user:%s" % current_user)
        
@oauth.before_request
def limit_client_request():
    client_id = request.values.get('client_id')
    if client_id is None:
        client_id = request.headers['client_id']
    app.logger.debug("Client_id:{client_id}".format(client_id=client_id))
    models.Client.objects(id=client_id).first().queries_left -= 1
    pprint (request.headers)
#     if not client_id:
#         return
#     client = Client.get(client_id)
#     if over_limit(client):
#         return abort(403)
#     track_request(client)

@login_manager.user_loader
def load_user(user_id):
    try:
        app.logger.debug("Inside load_user with user id:" + user_id)
        return models.User.objects(id=user_id).first()
    except ValidationError:
        return None
        
@app.route('/login', methods = ['GET', 'POST'])
def login(*args, **kwargs):
    if g.user is not None and g.user.is_authenticated():
        app.logger.debug("Inside login view. g.user is not None or g.user.is_authenticated")
        return redirect(url_for("index"))
    form = LoginForm()
    next = request.args.get("next")
    if next is not None:
        session['next'] = next
        app.logger.debug("######### Value of 'session.next' is {next}".format(next=session['next']))
    if form.validate_on_submit():
        redirect_view_function = 'index'
        app.logger.debug("Username: %s, Password: %s \n" % (form.username.data, form.password.data))
        user = check_auth_return_user(form.username.data, form.password.data)
        if user is not None:
            app.logger.debug("Username: %s" % user.username)
            app.logger.debug("user_id: %s" % user.get_id())
            session['user'] = user.username
            login_user(user)
            app.logger.debug("Value of 'next' is {next}".format(next=session['next']))
            return redirect(session['next'] or url_for("dashboard"))
        return redirect(url_for("login", next=session['next']))
    return render_template('login.html',
        title = 'Sign In',
        user = g.user,
        web_content_ui=web_content.ui_elements,
        page="login_splash",
        form = form)

@app.route('/dashboard')
@login_required
def dashboard():
    client_list = models.Client.objects()
    for client in client_list:
        pprint (client.client_app_meta)
    return render_template('dashboard.html',
        web_content_ui=web_content.ui_elements,
        user = g.user,
        client_list = client_list,
        )

@app.route('/app_register', methods = ['GET', 'POST'])
@login_required
def app_register():
    form = ClientRegistrationForm()
    if form.validate_on_submit():
        app.logger.debug("""
            client_name:%s\n
            is_confidential:%s\n
            redirect_uris:%s\n
            default_scopes:%s\n
            client_description:%s\n
            client_secret:%s\n""" % (form.client_name.data, form.is_confidential.data,
            form.redirect_uris.data.split(), form.default_scopes.data.split(),
            form.client_description.data, random_id_generator() ))
        client_meta = {}
        for field in request.values.keys():
            field_type = field.split("_")[0]
            if field_type in custom_fields.base.__all__:
                client_meta[request.values.get(field)] = field.split("_")[0]
        pprint (client_meta)
        new_client = models.Client(
            client_name=form.client_name.data,
            is_confidential=form.is_confidential.data,
            redirect_uris=str(form.redirect_uris.data).split(),
            default_scopes=['email'], #TODO: Define multiple scopes str(form.default_scopes.data).split(),
            client_description=form.client_description.data,
            client_secret = random_id_generator(),
            client_app_meta = client_meta
        )
        new_client.save()
        return redirect('/dashboard')
    return render_template('app_register.html',
        web_content_ui=web_content.ui_elements,
        form = ClientRegistrationForm(),
        user = g.user,
        )


@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect('/')
        
def check_auth_return_user(username, password):
    user = models.User.objects(username=username).first()
    if user is not None and (user.username == username and user.password == password):
        app.logger.debug("User: %s successfully authenticated!" % user.username)
        return user
    return None
    
def baresniff_authentication_check(username, password, redirect_view_function):
    user = models.User.objects(username=username).first()
    app.logger.debug("<baresniff.views.baresniff_authentication_check()> User from database: %s" % user.username)
    if user is not None and (user.username == username and user.password == password):
        g.user = user
        app.logger.debug("Logged the user `%s` successfully!\n" % g.user.username)
        return True
    return False
    
@app.route('/index')
@login_required
def index():
    user = g.user
    app.logger.debug("Logged in username:`%s`!\n" % user.username)
    return render_template('index.html',
        user = user,
        title = "Welcome to baresniff")

# @app.route('/client-registration', methods = ['GET', 'POST'])
# @login_required
# def client_registration():
#     form = ClientRegistrationForm()
#     if form.validate_on_submit():
#         app.logger.debug("""
#             client_name:%s\n
#             is_confidential:%s\n
#             redirect_uris:%s\n
#             default_scopes:%s\n
#             client_description:%s\n
#             client_secret:%s\n""" % (form.client_name.data, form.is_confidential.data,
#             form.redirect_uris.data.split(), form.default_scopes.data.split(),
#             form.client_description.data, random_id_generator() ))
#         new_client = models.Client(
#             client_name=form.client_name.data,
#             is_confidential=form.is_confidential.data,
#             redirect_uris=str(form.redirect_uris.data).split(),
#             default_scopes=str(form.default_scopes.data).split(),
#             client_description=form.client_description.data,
#             client_secret = random_id_generator()
#         )
#         new_client.save()
#         return render_template('client-registration.html',
#             user = g.user,
#             client = new_client,
#             fresh_registration = "success"
#         )
#     return render_template('client-registration.html',
#         user = g.user,
#         form = ClientRegistrationForm(),
#         fresh_registration = "",
#         title = "Enter Details For The Client")
        
@app.route('/user-registration', methods=['POST', 'GET'])
def user_registration():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        app.logger.debug("""
            username:{username}\n
            password:{password}\n  
            email:{email}\n
            first_name:{first_name}\n
            last_name:{last_name}\n""".format(username=form.username.data, 
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data))
        user = models.User(username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data)
        user.save() #TODO: Exception handling
        return render_template('user-registration.html',
            form=form,
            user=user,
            registration='success')
    return render_template('user-registration.html',
        form=form,
        registration='new')
                
@app.route('/getusers', methods=['GET'])
#@login_required
@oauth.require_oauth('email')
def get_users(data):
#     user = data.user
#     app.logger.debug("Inside getusers method")
#     pprint (data)
#     pprint (user)
#     users = JSONEncoder().encode(models.User.objects().first())
#     pprint (type(users))
#     return users #flask.jsonify(**users)
    ret = "blah"
    return ret
        
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, models.User):
            return str(o)
        return json.JSONEncoder.default(self, o)
# @app.route('/favicon.ico')
# def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
        
@app.route('/')
def landing_page():
    user = current_user
    form = UserRegistrationForm()
    if current_user.is_anonymous() == True:
        user.username = "guest"
    return render_template('base.html',
        web_content_marketing=web_content.marketing_content,
        web_content_ui=web_content.ui_elements,
        user=user,
        page="landing",
        form=form)
        
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = UserRegistrationForm()
    pprint (form)
    if form.validate_on_submit():
        app.logger.debug("""
            username:{username}\n
            password:{password}\n  
            email:{email}\n
            first_name:{first_name}\n
            last_name:{last_name}\n""".format(username=form.username.data, 
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data))
        user = models.User(username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data)
        user.save() #TODO: Exception handling
        return render_template('user-registration.html',
            form=form,
            user=user,
            registration='success')
    return render_template('base-bootstrap.html',
        web_content_marketing=web_content.marketing_content,
        web_content_ui=web_content.ui_elements,
        form=form,
        username='guest')
        
@app.route('/tutorials')
def tutorial():
    return render_template('tutorial.html',
        web_content_marketing=web_content.marketing_content,
        web_content_ui=web_content.ui_elements,
        user = g.user,
        )
