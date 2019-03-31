
import json, arrow

from typing import Dict, Any, Union

from peewee import Model, TextField

from lncityapi.other.common import lncity_db


class BaseModel(Model):

    def __init__(self, fields):
        super().__init__()
        self._fields = fields

    class Meta:
        database = lncity_db

    @staticmethod
    def serializable_field_value(field_value, field_type, field_fields):
        if field_value is None:
            return None

        if field_type == 'base':
            return field_value
        elif field_type == 'date':
            return arrow.get(field_value).format()
        elif field_type == 'model':
            return field_value.serializable(field_fields)

    def serializable(self, fields: Dict[str, Union[bool, dict]] = None) -> Dict[str, Any]:
        if fields is None:
            fields = {}

        return {
            field_name: self.serializable_field_value(
                getattr(self, field_name),
                field_info.get('type', 'base'),
                fields.get(field_name).get('fields') if isinstance(fields.get(field_name), dict) else None
            )
            for field_name, field_info in self._fields.items()
            if (
                fields.get(field_name, field_info.get('show', False))
                if isinstance(fields.get(field_name), bool) else
                fields.get(field_name, {}).get('show', field_info.get('show', False))
            )
        }


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)
