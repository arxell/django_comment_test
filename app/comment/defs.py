from django.conf import settings

from schematics import types as t
from schematics.models import Model
from schematics.exceptions import ValidationError


class BaseModelIn(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate(strict=False)


class BaseModelOut(Model):
    STATUS_OK = 'ok'
    STATUS_ERROR = 'error'

    status = t.StringType(
        required=True,
        choices=[STATUS_OK, STATUS_ERROR],
    )

    ERROR_INVALID_INPUT_DATA = 'invalid_input_data'

    error = t.StringType(required=False)
    error_extra = t.StringType(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate(strict=False)

    @property
    def is_status_ok(self):
        return self.status == self.STATUS_OK


### add ###
class AddSchemIn(BaseModelIn):
    type_id = t.IntType(
        required=False,
        choices=settings.COMMENT_TYPES_LIST,
    )
    object_id = t.IntType(required=False, min_value=1)
    parent_id = t.IntType(required=False, min_value=1)
    text = t.StringType(required=True, min_length=1)
    user_id = t.IntType(required=True, min_value=1)

    def validate(self, *args, **kwargs):
        super().validate(*args, **kwargs)

        if self.parent_id and not (self.object_id and self.type_id):
            # comment for another comment
            pass
        elif not self.parent_id and (self.object_id and self.type_id):
            # comment for some object
            pass
        else:
            # invalid combination
            raise ValidationError(
                {'param': 'set parent_id or type_id/object_id'}
            )


class AddSchemOut(BaseModelOut):
    ERROR_PARENT_NOT_FOUND = 'parent_not_found'


### edit ###
class EditSchemIn(BaseModelIn):
    comment_id = t.IntType(required=True, min_value=1)
    text = t.StringType(required=True, min_length=1)
    user_id = t.IntType(required=False, min_value=1)


class EditSchemOut(BaseModelOut):
    ERROR_COMMENT_NOT_FOUND = 'comment_not_found'


### edit history ###
class EditHistorySchemIn(BaseModelIn):
    comment_id = t.IntType(required=True, min_value=1)


class EditHistorySchemOut(BaseModelOut):
    ERROR_COMMENT_NOT_FOUND = 'comment_not_found'


### delete ###
class DeleteSchemIn(BaseModelIn):
    comment_id = t.IntType(required=True, min_value=1)
    user_id = t.IntType(required=False, min_value=1)


class DeleteSchemOut(BaseModelOut):
    ERROR_COMMENT_NOT_FOUND = 'comment_not_found'
    ERROR_COMMENT_HAS_CHILDREN = 'comment_has_children'


### tree ###
class TreeSchemIn(BaseModelIn):
    comment_id = t.IntType(required=False, min_value=1)
    object_id = t.IntType(required=False, min_value=1)
    type_id = t.IntType(required=False, min_value=1)

    def validate(self, *args, **kwargs):
        super().validate(*args, **kwargs)

        if (
            not self.comment_id and
            not self.object_id and
            not self.type_id
        ):
            raise ValidationError(
                {'param': 'set comment_id or type_id/object_id'}
            )


class TreeSchemOut(BaseModelOut):
    ERROR_COMMENT_NOT_FOUND = 'comment_not_found'


### user history ###
class UserHistorySchemaIn(BaseModelIn):
    FORMAT_XML = 'xml'
    FORMAT_CSV = 'csv'

    user_id = t.IntType(required=True, min_value=1)
    created_at_from = t.DateTimeType(required=False)
    created_at_to = t.DateTimeType(required=False)
    format = t.StringType(
        required=False,
        choices=[FORMAT_XML, FORMAT_CSV],
    )

    @property
    def is_csv_format(self):
        return self.format == self.FORMAT_CSV

    @property
    def is_xml_format(self):
        return self.format == self.FORMAT_XML


class UserHistorySchemaOut(BaseModelOut):
    pass


### export ###
class ExportSchemaIn(BaseModelIn):
    FORMAT_XML = 'xml'
    FORMAT_CSV = 'csv'
    FORMAT_JSON = 'json'

    user_id = t.IntType(required=False, min_value=1)
    object_id = t.IntType(required=False, min_value=1)
    type_id = t.IntType(required=False, min_value=1)
    created_at_from = t.DateTimeType(required=False)
    created_at_to = t.DateTimeType(required=False)
    format = t.StringType(
        required=True,
        choices=[FORMAT_XML, FORMAT_CSV, FORMAT_JSON],
    )

    def validate(self, *args, **kwargs):
        super().validate(*args, **kwargs)

        if (
            not self.user_id and
            not self.object_id and
            not self.type_id
        ):
            raise ValidationError(
                {'param': 'set user_id or type_id/object_id'}
            )

    @property
    def is_csv_format(self):
        return self.format == self.FORMAT_CSV

    @property
    def is_xml_format(self):
        return self.format == self.FORMAT_XML


class ExportSchemaOut(BaseModelOut):
    pass


### export history ###
class ExportHistorySchemaIn(BaseModelIn):
    user_id = t.IntType(required=True, min_value=1)


class ExportHistorySchemaOut(BaseModelOut):
    pass


### export restore ###
class ExportRestoreSchemaIn(BaseModelIn):
    export_id = t.IntType(required=True, min_value=1)


class ExportRestoreSchemaOut(BaseModelOut):
    ERROR_EXPORT_NOT_FOUND = 'export_not_found'
    ERROR_BAD_EXPORT_DUMP = 'bad_export_dump'
