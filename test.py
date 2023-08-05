import os
import time

import initialize
from bot.self_drive_bot import SelfDriveBot
from model.openai import get_openai_llm
from repo.character import Character
from world.round_controller.time_base_controller import TimeBaseController
from world.world import BaseWorld

if __name__ == '__main__':
    # 初始化，一些数据库session和日志等公共组件
    initialize.initialize()
    # print(f'your key is {os.environ["open_ai_key"]}')

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录
    chr_me = Character.get_by_name("yuhua")
    chr_bot = Character.get_by_name("hero")

    # 构建一个bot，用于聊天
    bot = SelfDriveBot(llm=llm, tools=[], character=chr_bot)
    bot.start()
    # bot.interact("你记得你第一次溜冰是什么时候吗？", chr_me)

    tbc = TimeBaseController(60, 10)
    world = BaseWorld(tbc, "world")
    world.join(bot)
    world.start()

    time.sleep(1000000000)
