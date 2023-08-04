class HumanRole:

    def __init__(self):
        self.temp: str = ""

    def listen(self, message: str):
        self.temp = message
        print(message)

    def talk(self) -> str:
        query = input("")
        return query
