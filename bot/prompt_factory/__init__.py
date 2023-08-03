from pydantic import BaseModel


class BasePrompt(BaseModel):
    title: str


class Prompt(BasePrompt):
    pass

class Description(BasePrompt):
    content: str
    title: str
