from bot.config.base_prompt import get_base_prompt
from bot.prompt_factory.virtual_character import VirtualCharacter


class PromptFactory:
    def __init__(self, character: VirtualCharacter, base_space='    '):
        self.prompt = []
        self.base_prompt = get_base_prompt()
        self.character = character
        self.base_space = base_space
        self.prompt.append(self.base_prompt)

        self.prompt_build = None

    def pydantic2yaml(self):
        content_list = []
        for k, v in self.character.dict().items():
            self.dict2yaml(content_list, 0, k, v)
        return "".join(content_list)

    def dict2yaml(self, content_list, layer, key_of_value, value):

        content_list.append(f"{self.base_space * layer}Your {key_of_value.replace('_', ' ')}: \n")
        layer += 1
        spaces = self.base_space * layer
        for k, v in value.items():
            if isinstance(v, dict):
                content_list.append(f"{spaces}Your {key_of_value.replace('_', ' ')}: \n")
                self.dict2yaml(content_list, layer, k, v)
            elif isinstance(v, list):
                # 处理队列

                content_list.append(f"{spaces}Your {key_of_value.replace('_', ' ')}: \n")
                for idx, c in enumerate(v):
                    # 转成列表，列表有1. 2. 3. 4.
                    c = c.replace("\n", "").strip()
                    content_list.append(f'{spaces + self.base_space}{idx + 1}.{c}\n')
            else:
                # 直接处理
                v = v.replace("\n", "")
                v.strip()
                content_list.append(f"{spaces}Your {k.replace('_', ' ')}: {v}\n")

    def append(self, next_prompt: str):
        self.prompt.append(next_prompt)
        return self

    def build(self):
        self.prompt.append(self.pydantic2yaml())
        self.prompt_build = "\n".join(self.prompt)
        return self.prompt_build

    def __str__(self):
        return self.prompt_build
