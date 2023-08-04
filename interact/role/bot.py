from pydantic import BaseModel

from bot.core import Agent, Bot
from repo.character import Character


class BotRole:
    def __init__(self, bot_instance: Bot):
        self.bot_instance = bot_instance

    temp: str = ""

    def listen(self, message: str):
        self.temp = message

    def talk(self, character: Character) -> str:
        return self.bot_instance.interact(self.temp, character)

    @property
    def me(self):
        return self.bot_instance.brain.character

