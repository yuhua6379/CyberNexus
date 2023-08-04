from pydantic import BaseModel

from bot.core import Bot
from interact.command_line_interact import CommandLineInteracter
from interact.role.bot import BotRole
from interact.role.human import HumanRole
from repo.character import Character


class HumanInteractWithBot(BaseModel):
    command_line: CommandLineInteracter

    def start(self, bot_instance: Bot):
        bot = None
        human = None

        while bot is None or human is None:
            if human is None:
                human_name = self.command_line.next("请输入human的角色名:\n")
                human = Character.get_by_name(human_name)

            if bot is None:
                bot_name = self.command_line.next("请输入bot的角色名:\n")
                bot = Character.get_by_name(bot_name)

        human_role = HumanRole()
        bot_role = BotRole(bot_instance=bot_instance)

        while True:
            print(f"{human.name} says to {bot.name}:")
            message = human_role.talk()
            bot_role.listen(message)

            print(f"{bot.name} says to {human.name}:")
            message = bot_role.talk(human)
            human_role.listen(message)
