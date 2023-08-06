from bot.message import Message
from bot.self_drive_bot import SelfDriveBot
from interact.base_interact_tool import BaseInteractTool

from repo.character import Character

from world.botbroker import SyncBotBroker
from world.world import TurnBaseWorld


class HumanInteractWithBot(BaseInteractTool):

    def __init__(self, llm, tools, human=None, bot=None):
        self.human = human
        self.bot = bot
        self.llm = llm
        self.tools = tools
        self.world = TurnBaseWorld(steps_of_round=5, broker=SyncBotBroker())
        self.bot_instance = None
        self.inject_prompt = ""

        self.counting = 0

    def call(self, message: str):
        try:
            message = message.strip()

            if message.startswith("--help"):
                return """
                --help 帮助
                --human= 设置human角色
                --bot= 设置bot角色
                --prompt= 强制性注入一段prompt用于调试，该prompt暂时缓存，每次都会自动注入，再次调用会覆盖
                --prompt_clear 清理掉注入的prompt
                
                普通情况的输入视为human角色对bot角色的交互
                如果输入带||符号，前半段是动作，后半段是对话
                """

            if message.startswith("--prompt="):
                self.inject_prompt = message.replace("--prompt=", "")
                return "现在的注入prompt:\n" + self.inject_prompt

            if message.startswith("--prompt_clear"):
                self.inject_prompt = ""
                return "现在的注入prompt:\n" + self.inject_prompt

            if message.startswith("--human="):
                human_name = message.replace("--human=", "")
                self.human = Character.get_by_name(human_name)
                return f"设定为{self.human.name}"

            if message.startswith("--bot="):
                bot_name = message.replace("--bot=", "")
                self.bot = Character.get_by_name(bot_name)
                return f"设定为{self.bot.name}"

            if self.human is None:
                return "请输入--human={name}来设定你的角色"
            if self.bot is None:
                return "请输入--bot={name}来设定对话机器人的角色"

            if self.bot_instance is None:
                self.bot_instance = SelfDriveBot(llm=self.llm, tools=self.tools, character=self.bot)
                self.world.join(self.bot_instance)


            if message.find("||") != -1:
                message = message.split("||")
            else:
                message = ["", message]

            if self.counting % 5 == 0:
                # 设定交互5次就改变一次日程
                self.world.run()
            self.counting += 1
            self.bot_instance.set_debug_prompt(self.inject_prompt)
            ret = self.bot_instance.interact(Message(
                from_character=self.human.name,
                to_character=self.bot.name,
                action=message[0],
                message=message[1]), self.human)

            return f"动作：{ret.action}\n对话：{ret.message}"

        except:
            import traceback
            traceback.print_exc()
            return "出现了奇怪的错误，自己看日志咯"
