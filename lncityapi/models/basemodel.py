
import json, arrow

from typing import Dict, Any, Union

from lncityapi import db


def deep_clone(d: dict) -> dict:
    nd = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nd[k] = deep_clone(v)
        else:
            nd[k] = v

    return nd


def deep_update(bd: dict, ud: dict) -> dict:
    for k, v in ud.items():
        if isinstance(v, dict) and isinstance(bd.get(k), dict):
            bd[k] = deep_update(bd.get(k), v)
        else:
            bd[k] = v

    return bd


class BaseModel(db.Model):
    __abstract__ = True

    @staticmethod
    def serializable_field_value(field_value, field_type, field_fields):
        if field_value is None:
            return None

        if field_type == 'base':
            return field_value
        elif field_type == 'date':
            return arrow.get(field_value).format()
        elif field_type == 'model':
            if isinstance(field_value, list):
                return [v.serializable(field_fields) for v in field_value]
            else:
                return field_value.serializable(field_fields)

    def serializable(self, fields: Dict[str, Union[bool, dict]] = None) -> Dict[str, Any]:
        if fields is None:
            fields = {}

        serialization_fields = deep_clone(self._fields)
        serialization_fields = deep_update(serialization_fields, fields)

        _serializable = {}
        for field_name, field_info in serialization_fields.items():
            if isinstance(field_info, dict) and field_info.get('show', False):
                try:
                    field_value = getattr(self, field_name)
                except Exception as e:
                    field_value = None
                _serializable[field_name] = self.serializable_field_value(
                    field_value,
                    field_info.get('type', 'base'),
                    field_info.get('fields', {})
                )
            elif isinstance(field_info, bool) and field_info:
                try:
                    field_value = getattr(self, field_name)
                except Exception as e:
                    field_value = None
                _serializable[field_name] = self.serializable_field_value(field_value, 'base', {})

        return _serializable
