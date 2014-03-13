from datetime import datetime, timedelta
from flask import url_for, g, session, request
from baresniff import db, app, oauth
from baresniff import fields as custom_fields

from flask.ext.login import login_user, logout_user, current_user, login_required

from pprint import pprint

######TODO: Move all routes to a separate module####

#TODO: Proper comments, descriptions to be added

#TODO: Make sure that created_at field is never pushed from the user via api. 
#It should always be the server time.
   
class User(db.Document):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    username = db.StringField(max_length=30, unique=True, required=True)
    #TODO: hashed values stored (at the time of user creation) - add a salt for more security
    password = db.StringField(required=True) 
    email = db.EmailField(required=True)
    first_name = db.StringField(max_length=50, required=True)
    last_name = db.StringField(max_length=50, required=True)
    
# The is_authenticated method has a misleading name. 
# In general this method should just return True unless
#  the object represents a user that should not be allowed to authenticate for some reason.
    def is_authenticated(self):
        return True 
        
    def is_active(self):
        #TODO: Implement is_active - check an 'is_active' flag in the user model
        return True #if the user is active, might need an is_active boolean in the class
        
    def is_anonymous(self):
        #TODO: Implement is_anonymous
        return False #is the user exists
        
    def get_id(self):
        #returns a unicode identifying the user
        return unicode(self.id)
        
    def __unicode__(self):
        return self.username
    
#OAuth client
class Client(db.Document):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    client_secret = db.StringField(unique=True, required=True)
    is_confidential = db.BooleanField()
    redirect_uris = db.ListField(db.URLField())
    default_scopes = db.ListField(db.StringField())
    
    client_app_meta = db.DictField(field=db.StringField())
    
    #TODO: Implement these
    #allowed_grant_types
    #allowed_response_types
    #validate_scopes #A function to validate scopes
    
    client_name = db.StringField(max_length=100)
    client_description = db.StringField(max_length=255)
    #user = db.ReferenceField(User) #required when supporting client credential
    
    ## client book-keeping properties
    access_level = db.StringField(default="Free Access")
    queries_left = db.LongField(default=5000)
    
    ## client custom messages, etc.
    oauth_authorize_message = db.StringField(default="This app is using Baresniff APIs \
        to provide you a reliable service. Click 'Approve' below to continue.")

#TODO: Think of a way to get this to work!        
#     @property
#     def oauth_authorize_message(self):
#         oauth_authorize_message = db.StringField(default="{client_name} is using Baresniff APIs \
#             to provide you a reliable service. Click 'Approve' below to continue.".format(self.client_name))
#         return oauth_authorize_message

##Not required since we are using a ListField() for the uris    
#     @property
#     def redirect_uris(self):
#         if self._redirect_uris:
#             return self._redirect_uris.split()
#         return []
    
    @property
    def client_id(self):
        return self.id
        
    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]
    
    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'
        
class Grant(db.Document):
    user_id = db.StringField()
    user = db.ReferenceField(User)
    client_id = db.StringField()
    client = db.ReferenceField(Client)
    code = db.StringField()
    redirect_uri = db.StringField()
    expires = db.DateTimeField()
    scopes = db.ListField()
    
    #for soft-deleting the grant
    is_deleted = db.BooleanField(default=False)
    
    @property
    def user_id(self):
        return self.user.id
        
    @property
    def client_id(self):
        return self.client.id
        
    def delete(self):
        self.is_deleted = True

class Token(db.Document):
    client = db.ReferenceField(Client)
    user = db.ReferenceField(User)
    token_type = db.StringField()
    access_token = db.StringField()
    refresh_token = db.StringField()
    expires = db.DateTimeField()
    scopes = db.ListField()
    
    @property
    def client_id(self):
        return self.client.id
        
    @property
    def user_id(self):
        return self.user.id
        
class Sniff(db.Document):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('sniff', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", required=True) #TODO: get authenticated user

# mongoengine.fields.__all__ = __all__ = ['StringField',  'URLField',  'EmailField',  'IntField',  'LongField',
#            'FloatField',  'DecimalField',  'BooleanField',  'DateTimeField',
#            'ComplexDateTimeField',  'EmbeddedDocumentField', 'ObjectIdField',
#            'GenericEmbeddedDocumentField',  'DynamicField',  'ListField',
#            'SortedListField',  'DictField',  'MapField',  'ReferenceField',
#            'GenericReferenceField',  'BinaryField',  'GridFSError',
#            'GridFSProxy',  'FileField',  'ImageGridFsProxy',
#            'ImproperlyConfigured',  'ImageField',  'GeoPointField', 'PointField',
#            'LineStringField', 'PolygonField', 'SequenceField',  'UUIDField']

               
class BaseSniff(db.Document):
    user = db.ReferenceField(User, required=True)
#     _client = db.ReferenceField(Client)
    created_at = db.DateTimeField(default=datetime.now, required=True)
    custom_field_dict = custom_fields.CustomFieldDict(field=custom_fields.BaseCustomField())

    @property
    def client(self):
        pprint (request.values.get('client_id'))
        return Client.objects(id=request.values.get('client_id')).first()
        
    @property
    def user(self):
        pprint (request.get_json()['user_id'])
        return User.objects(id=request.get_json()['user_id'])

    def clean(self):
        """Validation to check if the values provided for 'custom_field_dict' map correctly
        to the structure defined in 'client_app_meta' defined at client creation."""
        if not self.client_meta_to_custom_field_mapper():
            #TODO: Have a better validation exception message!
            msg = "Custom fields do not match with the client_meta information"
            raise ValidationException(msg) 
        super(BaseSniff, self).save(*args, **kwargs)
        
    def client_meta_to_custom_field_mapper(self):
        client = self.client
        #TODO: RaiseException if client is None
        if client is not None:
            client_app_meta = client.client_app_meta
            for key in self.custom_field_dict:
                """Compares name function of CustomFields with string value stored against
                that name in Client.client_meta_app"""
                if not custom_field_dict[key].name == client_app_meta[key]:
                    return True #False #changed to test without validation
            return True
            
    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }
    
#     def save(self, *args, **kwargs):
#         pprint (self)
#         super(BaseSniff, self).save(*args, **kwargs)
    
       
        