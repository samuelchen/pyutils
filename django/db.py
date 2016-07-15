from django.db.models import UUIDField
import uuid


class UUIDIntField(UUIDField):
    # description = 'Integer format universally unique identifier'
    #
    # def get_internal_type(self):
    #     return "UUIDField"
    #
    # def get_db_prep_value(self, value, connection, prepared=False):
    #     if value is None:
    #         return None
    #     if not isinstance(value, uuid.UUID):
    #         try:
    #             value = uuid.UUID(value)
    #         except AttributeError:
    #             raise TypeError(self.error_messages['invalid'] % {'value': value})
    #
    #     if connection.features.has_native_uuid_field:
    #         return value
    #     return value.int

    pass