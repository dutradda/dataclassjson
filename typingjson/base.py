import dataclasses
from logging import getLogger
from typing import (  # type: ignore
    Any,
    Iterable,
    Optional,
    Type,
    _TypedDictMeta,
)

from .fields import DeserializeFields, SerializeFields
from .serializers import OrjsonDefaultTypes


logger = getLogger(__name__)


def typingjson(
    type_: Optional[Type[Any]] = None,
    deserialize_fields: Optional[Iterable[str]] = None,
    serialize_fields: Optional[Iterable[str]] = None,
) -> Any:
    def wrap(type__: Type[Any]) -> Any:
        if isinstance(type__, _TypedDictMeta):
            set_typed_dict_fields(type__)

        else:
            type__ = dataclasses.dataclass(type__)
            OrjsonDefaultTypes.set_type(type__)

        if deserialize_fields is not None:
            DeserializeFields.set_type(type__, deserialize_fields)
        else:
            DeserializeFields.clean_fields(type__)

        if serialize_fields is not None:
            SerializeFields.set_type(type__, serialize_fields)
        else:
            SerializeFields.clean_fields(type__)

        return type__

    if type_:
        return wrap(type_)

    return wrap


def set_typed_dict_fields(typed_dict_type: _TypedDictMeta) -> None:
    fields = {}

    for name, type_ in typed_dict_type.__annotations__.items():
        default = getattr(typed_dict_type, name, dataclasses.MISSING)

        if isinstance(default, dataclasses.Field):
            fields[name] = default

        else:
            fields[name] = dataclasses.field(default=default)
            fields[name].name = name
            fields[name].type = type_
            fields[name]._field_type = dataclasses._FIELD  # type: ignore

    typed_dict_type.__dataclass_fields__ = fields
