from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SelectMultipleField
from wtforms.validators import Required

class UserRegistrationForm(Form):
    username = TextField('Username', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    confirm_password = PasswordField()
    email = TextField('Email', validators = [Required()])
    first_name = TextField('First Name', validators = [Required()])
    last_name = TextField('Last Name', validators = [Required()])

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    
class ClientRegistrationForm(Form):
    client_id = TextField('client_id') #generated at the back-end
    client_secret = TextField('client_secret') #not displayed during registration
    is_confidential = BooleanField()
    redirect_uris = TextField() #TODO: Get a list of URIs
    default_scopes = TextField() #TODO: Get a list of scopes
    client_name = TextField('client_name', validators=[Required()])
    client_description = TextField('client_description')
    
class ResourceOwnerAuthorizeForm(Form):
    client_id = TextField('client_id')
    #scopes = SelectMultipleField('scopes')
    scope = TextField('Scope', validators=[Required()])
    #confirm = BooleanField()