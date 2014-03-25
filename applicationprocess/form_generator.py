import logging

from django import forms
from django.db import transaction

logger = logging.getLogger(__name__)
_global_cache = {}

class CustomForm( forms.Form ):
    @transaction.commit_on_success
    def save(self):
        if self.user_form.signed_copy:
            self.user_form.signed_copy.delete()
        self.user_form.form_data = self.cleaned_data
        self.user_form.save()

class FormFactory( object ):
    @staticmethod
    def form_from_user_form( user_form ):
        FormClass = FormFactory.form_from_database( user_form.form )
        FormClass.user_form = user_form

        return FormClass

    @staticmethod
    def form_from_database( form_model ):
        # dict() converts a list in the form [(1,2), (2,4)] in a dictionary {1:2, 2:4}
        return type( str(form_model.name), (CustomForm,), dict(FormFactory._get_fields( form_model )))

    @staticmethod
    def _get_fields( form_model ):
        """
        Fetches widgets from database and create the right objects.
        """
        return [FormFactory._field_object_from_db( db_field ) for db_field in form_model.fields.all() ]

    @staticmethod
    def _field_object_from_db( db_field ):
        """
        Returns (<field_name>, <field_object>)
        """
        field_class = FormFactory._get_object_class( 'field', db_field.type.target_class)
        validators = [FormFactory._validator_object_from_db(validator) for validator in db_field.validators.all()]
        options = db_field.extra_options
        options['validators'] = validators
        options['required'] = db_field.required
        options['label'] = db_field.label
        field_object = field_class( **options )

        return ( db_field.name, field_object )

    @staticmethod
    def _validator_object_from_db( db_validator ):
        validator_class = FormFactory._get_object_class( 'validator', db_validator.type.target_class)
        options = db_validator.options

        return validator_class( **options )
    @staticmethod
    def _get_object_class( type, complete_class_name ):
        cache = FormFactory._get_cache_for( type )
        if complete_class_name not in cache:
            cache[complete_class_name] = custom_import( complete_class_name )

        return cache[complete_class_name]

    @staticmethod
    def _get_cache_for( type ):
        if type not in _global_cache:
            _global_cache[type] = {}
        return _global_cache[type]

def custom_import( complete_class_name ):
    complete_class_name=str(complete_class_name)
    tmp = complete_class_name.split( '.' )
    package = '.'.join( tmp[:-1] )
    class_name = tmp[-1]
    try:
        class_object = __import__( package, fromlist=[class_name] )
    except ImportError:
        logger.error( "Error trying to import {complete_class_name}. Package : {package}, Class : {class_name}".format(
            complete_class_name=complete_class_name, package=package, class_name=class_name))
        raise

    return getattr( class_object, class_name )
