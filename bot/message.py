from typing import Optional

from pydantic import BaseModel

from bot.config.base_conf import EMPTY_ACTION, EMPTY_MESSAGE


class Message(BaseModel):
    from_character: str
    to_character: str
    action: Optional[str] = EMPTY_ACTION
    message: Optional[str] = EMPTY_MESSAGE
    stop: int = 0

    def to_prompt(self, simple_string=False):
        if simple_string:
            return f'{self.from_character}的动作:{self.action}\n{self.from_character}对{self.to_character}说:{self.message}'
        import json
        return json.dumps(self.dict(), ensure_ascii=False)
