import os

import initialize
from bot.agent import Character
from bot.base_bot import SimpleChatBot
from bot.message import Message
from bot.toolkits.internet_tools.get_weather_information_in_china import get_weather_info_in_china
from bot.toolkits.system_tools.watch import watch
from model.openai import get_openai_llm

if __name__ == '__main__':
    # 初始化，一些数据库session和日志等公共组件
    initialize.initialize()
    # print(f'your key is {os.environ["open_ai_key"]}')

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['openai_api_key'])

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录
    chr_me = Character.get_by_name("hero")
    chr_bot = Character.get_by_name("镇长先生")

    # 构建一个bot，用于聊天
    bot1 = SimpleChatBot(llm=llm, tools= "", character=chr_bot)
    bot2 = SimpleChatBot(llm=llm, tools= "", character=chr_me)

    start = bot1.startInteract(chr_me)

    ret = bot2.interact(Message(from_character=chr_me.name,
                                to_character=chr_bot.name,
                                action=start.action,
                                message=start.message), chr_me)

    while True:
        stop = 0
        ret = bot1.interact(Message(from_character=chr_me.name,
                                    to_character=chr_bot.name,
                                    action=ret.action,
                                    message=ret.message), chr_me)
        stop = ret.stop + stop
        ret = bot2.interact(Message(from_character=chr_bot.name,
                                    to_character=chr_me.name,
                                    action=ret.action,
                                    message=ret.message), chr_bot)
        stop = ret.stop + stop

        if stop > 0:
            break



    print(ret.dict())
