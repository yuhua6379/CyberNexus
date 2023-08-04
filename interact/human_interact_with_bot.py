
from bot.core import Bot
from interact.base_interact_tool import BaseInteractTool

from repo.character import Character


class HumanInteractWithBot(BaseInteractTool):

    def __init__(self, llm, tools, human=None, bot=None):
        self.human = human
        self.bot = bot
        self.llm = llm
        self.tools = tools

    def call(self, message: str):
        try:
            message = message.strip()

            if message.startswith("/human="):
                human_name = message.replace("/human=", "")
                self.human = Character.get_by_name(human_name)
                return f"设定为{self.human.name}"

            if message.startswith("/bot="):
                bot_name = message.replace("/bot=", "")
                self.bot = Character.get_by_name(bot_name)
                return f"设定为{self.bot.name}"

            if self.human is None:
                return "请输入/human={name}来设定你的角色"
            if self.bot is None:
                return "请输入/bot={name}来设定对话机器人的角色"

            bot = Bot(llm=self.llm, tools=self.tools, character=self.bot)
            return bot.interact(message, self.human)
        except:
            import traceback
            traceback.print_exc()
            return "出现了奇怪的错误，自己看日志咯"

