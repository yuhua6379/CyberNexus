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

        self.current_round = None
        self.run_left_step = False

    def call(self, message: str):
        try:
            message = message.strip()

            if message.startswith("--help"):
                return """
                --help 帮助
                --human= 设置human角色，如果没有这个角色会马上创建一个
                --bot= 设置bot角色
                --prompt= 强制性注入一段prompt用于调试，该prompt暂时缓存，每次都会自动注入，再次调用会覆盖
                --prompt_clear 清理掉注入的prompt
                
                普通情况的输入视为human角色对bot角色的交互
                如果输入带||符号，第一项是动作，第二项是对话，第三项是是否继续交互
                """

            if message.startswith("--prompt="):
                self.inject_prompt = message.replace("--prompt=", "")
                return "现在的注入prompt:\n" + self.inject_prompt

            if message.startswith("--prompt_clear"):
                self.inject_prompt = ""
                return "现在的注入prompt:\n" + self.inject_prompt

            if message.startswith("--human="):
                human_name = message.replace("--human=", "")
                Character.create_if_not_exists(human_name)
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
                if len(message) < 3:
                    message.append("0")
            else:
                message = ["", message, "0"]

            if self.current_round is None:
                # 初始跑一次world
                self.world.run()
                self.current_round = self.world.round
            elif self.run_left_step:
                # 角色决定stop了，跑完整个round
                while self.current_round >= self.world.round:
                    # 跑到下一个round位置
                    self.world.run()

                self.current_round = self.world.round
                self.run_left_step = False

            message_in = Message(
                from_character=self.human.name,
                to_character=self.bot.name,
                action=message[0],
                message=message[1],
                stop=int(message[2])
            )

            self.bot_instance.set_debug_prompt(self.inject_prompt)
            message_out = self.bot_instance.interact(message_in, self.human)

            if message_in.stop == message_out.stop == 1:
                # 标记，下次对话后触发，跑完整个round
                self.run_left_step = True
                # 总结所有的东西
                self.bot_instance.conclude_interact()

            if message_out.action is not None and message_out.action.strip():
                return f"<span style='color:gray;'>*{message_out.action}*</span>       {message_out.message}"
            else:
                return message_out.message
        except:
            import traceback
            traceback.print_exc()
            return "出现了奇怪的错误，自己看日志咯"
