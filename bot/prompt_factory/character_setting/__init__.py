from typing import Optional

from pydantic import BaseModel


class CharacterSetting(BaseModel):
    long_term_purposes: str
    thinking_way: str
    talking_way: str
    basic_information: str
