from __future__ import absolute_import
from collections import namedtuple

from corehq.apps.app_manager.util import app_doc_types
from corehq.apps.change_feed.exceptions import MissingMetaInformationError
from couchforms.models import all_known_formlike_doc_types
from dimagi.utils.couch.undo import DELETED_SUFFIX
from pillowtop.feed.interface import ChangeMeta

GROUP_DOC_TYPES = ('Group', 'Group-Deleted')

WEB_USER_DOC_TYPES = ('WebUser', 'WebUser-Deleted')

MOBILE_USER_DOC_TYPES = ('CommCareUser', 'CommCareUser-Deleted')

CASE_DOC_TYPES = ('CommCareCase', 'CommCareCase-Deleted')

DOMAIN_DOC_TYPES = ('Domain', 'Domain-Deleted', 'Domain-DUPLICATE')

SYNCLOG_DOC_TYPES = ('SyncLog', 'SimplifiedSyncLog')

CASE = 'case'
FORM = 'form'
DOMAIN = 'domain'
META = 'meta'
COMMCARE_USER = 'commcare-user'
WEB_USER = 'web-user'
GROUP = 'group'
APP = 'app'


DocumentMetadata = namedtuple(
    'DocumentMetadata', ['raw_doc_type', 'primary_type', 'subtype', 'domain', 'is_deletion']
)


def get_doc_meta_object_from_document(document):
    raw_doc_type = _get_document_type(document)
    if raw_doc_type:
        primary_type = _get_primary_type(raw_doc_type)
        return _make_document_type(raw_doc_type, primary_type, document)


def _get_primary_type(raw_doc_type):
    if raw_doc_type in CASE_DOC_TYPES:
        return CASE
    elif raw_doc_type in all_known_formlike_doc_types():
        return FORM
    elif raw_doc_type in DOMAIN_DOC_TYPES:
        return DOMAIN
    elif raw_doc_type in MOBILE_USER_DOC_TYPES:
        return COMMCARE_USER
    elif raw_doc_type in WEB_USER_DOC_TYPES:
        return WEB_USER
    elif raw_doc_type in GROUP_DOC_TYPES:
        return GROUP
    elif raw_doc_type in app_doc_types():
        return APP
    else:
        # at some point we may want to make this more granular
        return META


def _make_document_type(raw_doc_type, primary_type, document):
    if primary_type == CASE:
        return _case_doc_type_constructor(raw_doc_type, document)
    elif primary_type == FORM:
        return _form_doc_type_constructor(raw_doc_type, document)
    elif primary_type == DOMAIN:
        return _domain_doc_type_constructor(raw_doc_type, document)
    else:
        return DocumentMetadata(
            raw_doc_type, primary_type, None, _get_domain(document), is_deletion(raw_doc_type)
        )


def _get_document_type(document_or_none):
    return document_or_none.get('doc_type', None) if document_or_none else None


def _case_doc_type_constructor(raw_doc_type, document):
    return DocumentMetadata(
        raw_doc_type, CASE, document.get('type', None), _get_domain(document), is_deletion(raw_doc_type)
    )


def _form_doc_type_constructor(raw_doc_type, document):
    return DocumentMetadata(
        raw_doc_type, FORM, document.get('xmlns', None), _get_domain(document), is_deletion(raw_doc_type)
    )


def _domain_doc_type_constructor(raw_doc_type, document):
    is_deletion_ = raw_doc_type == 'Domain-DUPLICATE' or is_deletion(raw_doc_type)
    return DocumentMetadata(
        raw_doc_type, DOMAIN, None, document.get('name', None), is_deletion_
    )


def _get_subtype(doc_type, document):
    if doc_type in ('CommCareCase', 'CommCareCase-Deleted'):
        return document.get('type', None)
    elif doc_type in all_known_formlike_doc_types():
        return document.get('xmlns', None)
    return None


def change_meta_from_doc(document):
    if document is None:
        raise MissingMetaInformationError('No document!')

    doc_id = document.get('_id', None)
    if not doc_id:
        raise MissingMetaInformationError("No doc ID!!")

    doc_type = _get_document_type(document)
    if not doc_type:
        raise MissingMetaInformationError("No doc_type: {}".format(doc_id))

    is_deletion_ = doc_type == 'Domain-DUPLICATE' or is_deletion(doc_type)
    return ChangeMeta(
        document_id=doc_id or document['_id'],
        document_rev=document.get('_rev', None),
        document_type=doc_type,
        document_subtype=_get_subtype(doc_type, document),
        domain=_get_domain(document),
        is_deletion=is_deletion_,
        backend_id=document.get('backend_id', None)
    )


def change_meta_from_doc_meta_and_document(doc_meta, document, data_source_type, data_source_name, doc_id=None):
    if doc_meta is None:
        raise MissingMetaInformationError(u"Couldn't guess document type for {}!".format(document))

    doc_id = doc_id or document.get('_id', None)
    if not doc_id:
        raise MissingMetaInformationError(u"No doc ID!!".format(document))
    return ChangeMeta(
        document_id=doc_id or document['_id'],
        document_rev=document.get('_rev', None),
        data_source_type=data_source_type,
        data_source_name=data_source_name,
        document_type=doc_meta.raw_doc_type,
        document_subtype=doc_meta.subtype,
        domain=doc_meta.domain,
        is_deletion=doc_meta.is_deletion,
    )


def _get_domain(document):
    return document.get('domain', None)


def is_deletion(raw_doc_type):
    # can be overridden
    return raw_doc_type is not None and raw_doc_type.endswith(DELETED_SUFFIX)
