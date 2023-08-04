import json
from enum import Enum
from typing import Type

from pydantic import BaseModel
from sqlalchemy import TypeDecorator, TEXT, VARCHAR


def gen_impl(impl, py_type):
    class NoName(impl):
        python_type = py_type

    return NoName


class Json(TypeDecorator):
    impl = gen_impl(TEXT, dict)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value:
            value = json.loads(value)

        return value


class JsonDict(Json):
    def process_bind_param(self, value, dialect):
        if type(value) != dict:
            raise TypeError("JsonDict must be dict")

        return super(JsonDict, self).process_bind_param(value, dialect)

    def process_result_value(self, value, dialect):
        value = super(JsonDict, self).process_result_value(value, dialect)
        if type(value) != dict:
            raise TypeError("JsonDict must be dict")

        return value


def SqlEnum(enum_type: Type[Enum]):
    class NoName(TypeDecorator):
        class ENUM(VARCHAR):
            python_type = enum_type

        impl = ENUM

        class NoNameEnum(BaseModel):
            enum_value: enum_type

        def process_bind_param(self, value, dialect):
            if value is not None:
                e = NoName.NoNameEnum(enum_value=value)
                return e.enum_value.value
            return None

        def process_result_value(self, value, dialect):
            if value is not None:
                e = NoName.NoNameEnum(enum_value=value)
                return e.enum_value
            return None

    return NoName(20)


def Pydantic(base_model: Type[BaseModel]):
    class NoName(TypeDecorator):

        impl = gen_impl(TEXT, base_model)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.base_model = base_model

        def process_bind_param(self, value: base_model, dialect):
            if value is not None:
                value = value.json()

            return value

        def process_result_value(self, value: str, dialect) -> base_model:
            if value:
                return self.base_model.parse_obj(json.loads(value))
            else:
                try:
                    # 尝试使用默认值
                    return self.base_model()
                except:
                    pass
            return None

    return NoName
