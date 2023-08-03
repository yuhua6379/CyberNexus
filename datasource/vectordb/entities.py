from typing import List

from pydantic import BaseModel


class Document(BaseModel):
    id: str
    meta_data: dict
    content: str


class Response(BaseModel):
    document: Document
    distance: float
