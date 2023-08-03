from pydantic import BaseModel

from bot.core import Bot


class BotRole(BaseModel):
    bot_instance: Bot

    temp: str = ""

    def listen(self, message: str):
        self.temp = message

    def talk(self) -> str:
        return self.bot_instance.chat(self.temp)

    @property
    def me(self):
        return self.bot_instance.character2

    @property
    def other(self):
        return self.bot_instance.character1
