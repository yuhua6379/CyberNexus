from pydantic import BaseModel

from repo.character import Character


class HumanRole(BaseModel):
    me: Character
    other: Character

    temp: str = ""

    def listen(self, message: str):
        self.temp = message
        print(message)

    def talk(self) -> str:
        query = input("")
        return query
