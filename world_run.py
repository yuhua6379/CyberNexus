import os

import initialize
from bot.agent import Character
from bot.base_bot import SimpleChatBot
from bot.message import Message
from bot.self_drive_bot import SelfDriveBot
from bot.toolkits.internet_tools.get_weather_information_in_china import get_weather_info_in_china
from bot.toolkits.system_tools.watch import watch
from model.openai import get_openai_llm
from world.botbroker import SyncBotBroker
from world.world import TurnBaseWorld

if __name__ == '__main__':
    # 初始化，一些数据库session和日志等公共组件
    initialize.initialize()
    # print(f'your key is {os.environ["open_ai_key"]}')

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['openai_api_key'])

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录
    chr_bot = Character.get_by_name("hero")

    bot_instance = SelfDriveBot(llm=llm, tools=[], character=chr_bot)

    world = TurnBaseWorld(steps_of_round=5, broker=SyncBotBroker())
    world.join(bot_instance)

    while True:
        world.run()
