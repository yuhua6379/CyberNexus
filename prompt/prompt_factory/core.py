from prompt.prompt_factory import Description, Prompt
from prompt.prompt_factory.virtual_character import VirtualCharacter


class PromptFactory:
    def __init__(self):
        self.prompt = []
    # def __init__(self, character: VirtualCharacter, base_space='    ', prefix=""):
    #
    #     self.character = character
    #     self.base_space = base_space
    #     self.prefix = prefix
    #     self.prompt = []
    #
    #     self.prompt_build = None
    #
    # def build_yaml_character_prompt(self):
    #     content_list = []
    #     for k in self.character.__fields_set__:
    #         self._process_members(content_list, 0, getattr(self.character, k))
    #     return "".join(content_list)
    #
    # def _process_description(self, content_list, layer, desc: Description):
    #     spaces = self.base_space * layer
    #     content_list.append(f"{spaces} {self.prefix}{desc.title}: {desc.content}\n")
    #
    # def _process_prompt(self, content_list, layer, prompt: Prompt):
    #     content_list.append(f"{self.base_space * layer}{self.prefix}{prompt.title}: \n")
    #     for k in prompt.__fields_set__:
    #         self._process_members(content_list, layer + 1, getattr(prompt, k))
    #
    # def _process_members(self, content_list, layer, prompt):
    #     if isinstance(prompt, Description):
    #         self._process_description(content_list, layer, prompt)
    #     if isinstance(prompt, Prompt):
    #         self._process_prompt(content_list, layer, prompt)
    #     if isinstance(prompt, list):
    #         for item in prompt:
    #             self._process_description(content_list, layer + 1, item)

    def append(self, next_prompt: str):
        self.prompt.append(next_prompt)
        return self

    # def build(self):
    #     self.prompt.append(self.build_yaml_character_prompt())
    #     self.prompt_build = "\n".join(self.prompt)
    #     self.prompt = []
    #     return self.prompt_build

    def build(self):
        prompt_build = "\n\n".join(self.prompt)
        # self.prompt = []
        return prompt_build

    # def __str__(self):
    #     return self.prompt_build
