from typing import List

from langchain.chat_models.base import BaseChatModel
from langchain.tools import BaseTool

from bot.agent import AgentBuilder
from bot.brain.brain import Brain
from bot.message import Message
from repo.character import Character


class BaseBot:
    def __init__(self, llm: BaseChatModel, tools: List[BaseTool], character: Character):
        self.character = character
        self.brain = Brain(character, AgentBuilder(llm=llm, tools=tools))

    def interact(self, message: Message, input_character: Character, debug: bool = True):
        return self.brain.react(message, input_character, debug)

    def startInteract(self, input_character: Character):
        return self.brain.startInteract(input_character)



    def set_debug_prompt(self, prompt: str):
        self.brain.set_debug_prompt(prompt)


class SimpleChatBot(BaseBot):
    """朴素，简单的，只能做普通一对一交互的机器人"""
    pass
