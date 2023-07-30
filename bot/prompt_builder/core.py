class PromptBuilder:
    def __init__(self):
        self.prompt = ""

    def append(self, next_prompt: str):
        self.prompt += '\n' + next_prompt

    def merge(self, l, r):
        self.prompt = self.prompt + "\n" + r.prompt

    def __str__(self):
        return self.prompt

