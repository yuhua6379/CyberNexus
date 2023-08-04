import os

import initialize
from bot.core import Bot
from bot.prompt_factory.core import PromptFactory
from bot.toolkits import get_weather_info_in_china
from bot.toolkits.system_tools import watch
from interact.command_line_interact import CommandLineInteracter
from interact.human_interact_with_bot import HumanInteractWithBot
from model.openai import get_openai_llm
from repo.character import Character

if __name__ == '__main__':
    initialize.initialize()
    interact = HumanInteractWithBot(command_line=CommandLineInteracter())

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录
    chr_me = Character.get_by_name("yuhua")
    chr_bot = Character.get_by_name("adam")

    # 构建一个bot，用于聊天
    bot = Bot(llm=llm, tools=[get_weather_info_in_china, watch], character=chr_bot)

    try:
        interact.start(bot)
    except CommandLineInteracter.StopException as e:
        print(e)
