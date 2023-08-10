import os
import initialize
from model.agent import Character
from bot.base_bot import SimpleChatBot
from model.entities.message import Message
from model.openai import get_openai_llm

if __name__ == '__main__':
    # 初始化，一些数据库session和日志等公共组件
    initialize.initialize()
    # print(f'your key is {os.environ["open_ai_key"]}')

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['openai_api_key'])

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录
    chr_me = Character.get_by_name("李华")
    chr_bot = Character.get_by_name("镇长先生")

    # 构建一个bot，用于聊天
    bot1 = SimpleChatBot(llm=llm, tools="", character=chr_bot)
    bot2 = SimpleChatBot(llm=llm, tools="", character=chr_me)

    start = bot1.meet(chr_me)

    ret = bot2.interact(Message(from_character=chr_bot.name,
                                to_character=chr_me.name,
                                action=start.action,
                                message=start.message), chr_bot)

    max_turn = 8

    while max_turn > 0:
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

        max_turn = max_turn - 1

    print(ret.dict())
