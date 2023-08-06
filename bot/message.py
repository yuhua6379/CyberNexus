from typing import Optional

from pydantic import BaseModel

from bot.config.base_conf import EMPTY_ACTION, EMPTY_MESSAGE


class Message(BaseModel):
    from_character: str
    to_character: str
    action: Optional[str] = EMPTY_ACTION
    message: Optional[str] = EMPTY_MESSAGE

    def __str__(self):
        import json
        return json.dumps(self.dict(), ensure_ascii=False)
        # return self.json()

