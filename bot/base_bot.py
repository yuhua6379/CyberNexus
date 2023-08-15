from typing import List

from langchain.chat_models.base import BaseChatModel
from langchain.tools import BaseTool

from bot.brain.brain import Brain
from model.agent import AgentBuilder
from model.base_prompt_factory import BasePromptFactory
from model.entities.message import Message
from repo.character import Character


class BaseBot:
    def __init__(self, llm: BaseChatModel, tools: List[BaseTool], character: Character, factory: BasePromptFactory):
        self.character = character
        self.brain = Brain(character, AgentBuilder(llm=llm, tools=tools), factory=factory)

    def interact(self, message: Message):
        return self.brain.react(message, Character.get_by_name(message.from_character))

    def meet(self, input_character: Character):
        return self.brain.stimulus_of_character(input_character)

    def conclude_interact(self):
        # 总结所有的交互
        self.brain.conclude_all(self.brain.st_memory.shrink(shrink_all=True))

    def set_debug_prompt(self, prompt: str):
        self.brain.set_debug_prompt(prompt)


class SimpleChatBot(BaseBot):
    """朴素，简单的，只能做普通一对一交互的机器人"""
    pass
