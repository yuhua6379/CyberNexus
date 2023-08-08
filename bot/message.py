from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    from_character: str
    to_character: str
    action: Optional[str] = ""
    message: Optional[str] = ""
    stop: int = 0

    def to_prompt(self, simple_string=False):
        if simple_string:
            return f'{self.from_character}的动作:{self.action}\n{self.from_character}对{self.to_character}说:{self.message}'
        import json
        return json.dumps(self.dict(), ensure_ascii=False)
