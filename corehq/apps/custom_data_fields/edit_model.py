import json

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.utils.translation import ugettext as _
from django import forms

from dimagi.utils.decorators.memoized import memoized
from dimagi.utils.forms import FormListForm

from .models import (CustomDataFieldsDefinition, CustomDataField,
                     validate_reserved_words)


class CustomDataFieldsForm(FormListForm):
    """
    The main form for editing a custom data definition
    """
    child_form_class = CustomDataFieldForm


class XmlSlugField(forms.SlugField):
    default_validators = [
        validate_slug,
        validate_reserved_words,
    ]


class CustomDataFieldForm(forms.Form):
    """
    Sub-form for editing an individual field's definition.
    """
    label = forms.CharField(
        required=True,
        error_messages={'required': _('All fields are required')}
    )
    slug = XmlSlugField(
        required=True,
        error_messages={
            'required': _('All fields are required'),
            'invalid': _('Key fields must consist only of letters, numbers, '
                         'underscores or hyphens.'),
        }
    )
    is_required = forms.BooleanField(required=False)
    choices = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, raw, *args, **kwargs):
        # Pull the raw_choices out here, because Django incorrectly
        # serializes the list and you can't get it
        self._raw_choices = filter(None, raw.get('choices', []))
        super(CustomDataFieldForm, self).__init__(raw, *args, **kwargs)

    def clean_choices(self):
        return self._raw_choices


class CustomDataModelMixin(object):
    """
    Provides the interface for editing the ``CustomDataFieldsDefinition``
    for each entity type.
    Each entity type must provide a subclass of this mixin.
    """
    urlname = None
    template_name = "custom_data_fields/custom_data_fields.html"
    field_type = None
    entity_string = None  # User, Group, Location, Product...

    @classmethod
    def get_validator(cls, domain):
        data_model = CustomDataFieldsDefinition.get_or_create(domain, cls.field_type)
        return data_model.get_validator(cls)

    @classmethod
    def page_name(cls):
        return _("Edit {} Fields").format(cls.entity_string)

    def get_definition(self):
        return CustomDataFieldsDefinition.get_or_create(self.domain,
                                                        self.field_type)

    def get_custom_fields(self):
        definition = self.get_definition()
        if definition:
            return definition.fields
        else:
            return []

    def save_custom_fields(self):
        definition = self.get_definition() or CustomDataFieldsDefinition()
        definition.field_type = self.field_type
        definition.domain = self.domain
        definition.fields = [
            self.get_field(field)
            for field in self.form.cleaned_data['data_fields']
        ]
        definition.save()

    def get_field(self, field):
        return CustomDataField(
            slug=field.get('slug'),
            is_required=field.get('is_required'),
            label=field.get('label'),
            choices=field.get('choices'),
        )

    @property
    def page_context(self):
        return {
            "custom_fields": json.loads(self.form.data['data_fields']),
            "custom_fields_form": self.form,
        }

    @property
    @memoized
    def form(self):
        if self.request.method == "POST":
            return CustomDataFieldsForm(self.request.POST)
        else:
            serialized = json.dumps([field.to_json()
                                     for field in self.get_custom_fields()])
            return CustomDataFieldsForm({'child_form_data': serialized})

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.save_custom_fields()
            msg = _(u"{} fields saved successfully").format(self.entity_string)
            messages.success(request, msg)
            return self.get(request, success=True, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)
