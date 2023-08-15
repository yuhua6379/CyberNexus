from collections import defaultdict
from typing import List, Tuple, Any

from langchain.chat_models.base import BaseChatModel
from langchain.tools import BaseTool

from model.agent import AgentBuilder
from bot.brain.brain import Brain
from model.entities.message import Message
from repo.character import Character


class BaseBot:
    def __init__(self, llm: BaseChatModel, tools: List[BaseTool], character: Character):
        self.character = character
        self.brain = Brain(character, AgentBuilder(llm=llm, tools=tools))

    def interact(self, message: Message, input_character: Character):
        return self.brain.react(message, input_character)

    def meet(self, input_character: Character):
        return self.brain.stimulus_of_character(input_character)

    def conclude_interact(self):
        # 总结所有的交互
        history_list = self.brain.st_memory.shrink(shrink_all=True)
        character_history_list_dict = defaultdict(list)
        for history in history_list:
            character_history_list_dict[(history.other_character.id, history.other_character)].append(history)
        for tp, item in character_history_list_dict.items():
            history_list = item
            other_character = tp[1]

            self.brain.conclude(history_list, other_character)

    def set_debug_prompt(self, prompt: str):
        self.brain.set_debug_prompt(prompt)


class SimpleChatBot(BaseBot):
    """朴素，简单的，只能做普通一对一交互的机器人"""
    pass
