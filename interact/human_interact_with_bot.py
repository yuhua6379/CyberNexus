from bot.base_bot import SimpleChatBot
from bot.message import Message
from bot.self_drive_bot import SelfDriveBot
from interact.base_interact_tool import BaseInteractTool

from repo.character import Character
from world.round_controller.turn_base_round_controller import TurnBaseController
from world.world import BaseWorld


class HumanInteractWithBot(BaseInteractTool):

    def __init__(self, llm, tools, human=None, bot=None):
        self.human = human
        self.bot = bot
        self.llm = llm
        self.tools = tools
        controller = TurnBaseController(10)
        self.world = BaseWorld(round_controller=controller, logger_name="world")
        self.bot_instance = None

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

            if self.bot_instance is None:
                self.bot_instance = SelfDriveBot(llm=self.llm, tools=self.tools, character=self.bot)
                self.world.join(self.bot_instance)

            ret = self.bot_instance.interact(Message(message=message), self.human)
            return f"动作：{ret.action}\n对话：{ret.message}"

        except:
            import traceback
            traceback.print_exc()
            return "出现了奇怪的错误，自己看日志咯"
