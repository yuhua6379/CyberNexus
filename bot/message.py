from typing import Optional

from pydantic import BaseModel

from bot.config.base_conf import DELIMITER, EMPTY_ACTION, EMPTY_MESSAGE


class Message(BaseModel):
    action: Optional[str] = EMPTY_ACTION
    message: Optional[str] = EMPTY_MESSAGE

    def __str__(self):
        return f'{self.action}{DELIMITER}{self.message}'
