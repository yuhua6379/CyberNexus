from bot.brain.brain import Brain
from model.base_prompt_factory import BasePromptFactory
from model.entities.message import Message
from model.llm import BaseLLM
from model.llm_broker import LLMBrokerBuilder
from model.prompt_broker import PromptBroker
from repo.character import Character


class BaseBot:
    def __init__(self, llm: BaseLLM, character: Character, factory: BasePromptFactory):
        self.character = character
        self.broker = PromptBroker(factory)
        self.brain = Brain(character, LLMBrokerBuilder(llm=llm), broker=self.broker)

    def interact(self, message: Message):
        return self.brain.react(message, Character.get_by_name(message.from_character))

    def meet(self, input_character: Character):
        return self.brain.provoked_by_character(input_character)

    def conclude_interactions(self):
        # 总结所有的交互
        self.brain.conclude_all(self.brain.st_memory.shrink(shrink_all=True))

    def set_debug_prompt(self, prompt: str):
        # 插入一段调试用的prompt
        self.broker.set_debug_prompt(prompt)

    def wake(self, situation):
        # world的轮动会wake自驱动机器人，机器人可以感受到各种情况
        # awake并且感知到了situation
        self.broker.set_situation(situation)

    def reschedule(self):
        self.brain.schedule()

    def make_impression(self, character: Character):
        self.brain.impress(character)


class SimpleChatBot(BaseBot):
    """朴素，简单的，只能做普通一对一交互的机器人"""
    pass
