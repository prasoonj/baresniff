from baresniff import db

class BaseCustomField(object):
    """All the custom fields that a client is provided to 'custom build' their Sniff
    must sub-class this base class"""
    pass
    
class CustomFieldDict(db.DictField):
    """A field that maps a name to a specified field type. Similar to
    a DictField, except the 'value' of each item must match the specified
    field type which should be a sub-class of BaseCustomField.
    """

    def __init__(self, field=None, *args, **kwargs):
        if not isinstance(field, BaseCustomField):
            self.error('Argument to CustomDictField constructor must be a valid '
                       'field')
        super(CustomFieldDict, self).__init__(field=field, *args, **kwargs)
        
# __all__ = ['StringField',  'URLField',  'EmailField',  'IntField',  'LongField',
#            'FloatField',  'DecimalField',  'BooleanField',  'DateTimeField',
#            'ComplexDateTimeField',  'EmbeddedDocumentField', 'ObjectIdField',
#            'GenericEmbeddedDocumentField',  'DynamicField',  'ListField',
#            'SortedListField',  'DictField',  'MapField',  'ReferenceField',
#            'GenericReferenceField',  'BinaryField',  'GridFSError',
#            'GridFSProxy',  'FileField',  'ImageGridFsProxy',
#            'ImproperlyConfigured',  'ImageField',  'GeoPointField', 'PointField',
#            'LineStringField', 'PolygonField', 'SequenceField',  'UUIDField']

__all__ = ['BaseCustomField', 'CustomFieldDict',
            'ShortTextField', 'LongTextField', 'CustomDateTimeField', 
            'CustomURLField', 'CustomEmailField', 'CustomIntField','CustomListField', 
            'CustomDictField','CustomFileField', 'CustomImageField', 'CustomGeoPointField',
            'PlaceObject', 'EventObject']

class ShortTextField(BaseCustomField, db.StringField):
    """"A string based field. Used for shorter text like 'titles', 'names', etc.
    must include a validation for maximum allowed characters in the string"""
    def __init__(self, **kwargs):
        super(ShortTextField, self).__init__(**kwargs)
        
    #TODO: A better way to finding names of the class
    def name(self):
        return 'ShortTextField'
        
    def validate(self, value):
        super(ShortTextField, self).validate(value)
        
class LongTextField(BaseCustomField, db.StringField):
    def __init__(self, **kwargs):
        super(LongTextField, self).__init__(**kwargs)
        
    def name(self):
        return 'LongTextField'
        
    def validate(self, value):
        super(LongTextField, self).__init__(**kwargs)

class CustomDateTimeField(BaseCustomField, db.DateTimeField):
    def __init__(self, **kwargs):
        super(CustomDateTimeField, self).__init__(**kwargs)
        
    def name(self):
        return 'CustomDateTimeField'
        
    def validate(self, value):
        super(CustomDateTimeField, self).__init__(**kwargs)
        
class CustomURLField(BaseCustomField, db.URLField):
    def __init__(self, **kwargs):
        super(CustomURLField, self).__init__(**kwargs)
        
    def name(self):
        return 'CustomURLField'
        
    def validate(self, value):
        super(CustomURLField, self).__init__(**kwargs)

class CustomEmailField(BaseCustomField, db.EmailField):
    def __init__(self, **kwargs):
        super(CustomEmailField, self).__init__(**kwargs)
        
    def name(self):
        return 'CustomEmailField'
        
    def validate(self, value):
        super(CustomEmailField, self).__init__(**kwargs)
        
class CustomIntField(BaseCustomField, db.IntField):
    def __init__(self, **kwargs):
        super(CustomIntField, self).__init__(**kwargs)
        
    def name(self):
        return 'CustomIntField'
        
    def validate(self, value):
        super(CustomIntField, self).__init__(**kwargs)

class CustomListField(BaseCustomField, db.ListField):
    def __init__(self, **kwargs):
        super(CustomListField, self).__init__(**kwargs)
        
    def name(self):
        return 'CustomListField'
        
    def validate(self, value):
        super(CustomListField, self).__init__(**kwargs)

class CustomDictField(BaseCustomField, db.DictField):
    def __init__(self, **kwargs):
        super(CustomDictField, self).__init__(**kwargs)
        
    def name(self):
        return 'CustomDictField'
        
    def validate(self, value):
        super(CustomDictField, self).__init__(**kwargs)

class CustomFileField(BaseCustomField, db.FileField):
    def __init__(self, **kwargs):
        super(CustomFileField, self).__init__(**kwargs)
        
    def name(self):
        return 'CustomFileField'
        
    def validate(self, value):
        super(CustomFileField, self).__init__(**kwargs)

class CustomImageField(BaseCustomField, db.ImageField):
    def __init__(self, **kwargs):
        super(CustomImageField, self).__init__(**kwargs)
        
    def name(self):
        return 'CustomImageField'
        
    def validate(self, value):
        super(CustomImageField, self).__init__(**kwargs)

class CustomGeoPointField(BaseCustomField, db.GeoPointField):
    def __init__(self, **kwargs):
        super(CustomGeoPointField, self).__init__(**kwargs)
        
    def name(self):
        return 'CustomGeoPointField'
        
    def validate(self, value):
        super(CustomGeoPointField, self).__init__(**kwargs)
        
class PlaceObject(BaseCustomField):
    place_name = db.StringField()
    place_location = db.GeoPointField()
    place_type = db.StringField() #can be a list of predefined types of place eg. pub
    
    def name(self):
        return 'PlaceObject'
        
class EventObject(BaseCustomField):
    event_name = db.StringField()
    event_location = db.GeoPointField()
    event_place = PlaceObject()
    
    def name(self):
        return 'EventObject'