from django.db import models


def _empty2none(value):
    """Represent empty strings as nulls"""
    if isinstance(value, basestring):
        value = value.strip()
    return value or None


class NullCharField(models.CharField):
    """CharField that stores empty strings as NULLs"""
    def get_prep_value(self, value):
        value = super(models.CharField, self).get_prep_value(value)
        return _empty2none(value)


class NullTextField(models.TextField):
    """TextField that stores empty strings as NULLs"""
    def get_prep_value(self, value):
        value = super(models.TextField, self).get_prep_value(value)
        return _empty2none(value)


class NullURLField(models.URLField):
    """URLField that stores empty strings as NULLs"""
    def get_prep_value(self, value):
        value = super(models.URLField, self).get_prep_value(value)
        return _empty2none(value)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['^contrib\.fields'])
