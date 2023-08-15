import os
import initialize
from bot.self_drive_bot import SelfDriveBot
from model.agent import Character

from model.entities.message import Message
from model.openai import get_openai_llm
import tool_build_character
from world.botbroker import SyncBotBroker
from world.world import TurnBaseWorld

tool_build_character.build()

if __name__ == '__main__':
    # 初始化，一些数据库session和日志等公共组件
    initialize.initialize()
    # print(f'your key is {os.environ["open_ai_key"]}')

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['openai_api_key'])

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录

    chr1 = Character.get_by_name("镇长先生")
    chr2 = Character.get_by_name("李华")

    # 构建一个bot，用于聊天
    bot1 = SelfDriveBot(llm=llm, tools=[], character=chr1)
    bot2 = SelfDriveBot(llm=llm, tools=[], character=chr2)

    world = TurnBaseWorld(steps_of_round=5, broker=SyncBotBroker())
    world.join(bot1)
    world.join(bot2)

    max_turn = 8
    current_turn = world.round
    for i in range(max_turn):

        # 一回合开始
        ret1 = bot1.meet(chr2)
        ret2 = bot2.interact(ret1)

        print(ret1.to_prompt())
        print(ret2.to_prompt())

        while True:
            if ret1.stop == ret2.stop == 1:
                print("对话结束")
                break
            ret1 = bot1.interact(ret2)

            ret2 = bot2.interact(ret1)

            print(ret1.to_prompt())
            print(ret2.to_prompt())

        # 互相生成印象
        bot1.make_impression(chr2)
        bot2.make_impression(chr1)

        bot1.conclude_interact()
        bot2.conclude_interact()

        # 角色决定stop了，跑完整个round
        while current_turn >= world.round:
            # 跑到下一个round位置
            world.run()
        current_turn = world.round

    # while max_turn > 0:
    #     stop = 0
    #     ret = bot1.interact(Message(from_character=chr_me.name,
    #                                 to_character=chr_bot.name,
    #                                 action=ret.action,
    #                                 message=ret.message), chr_me)
    #     stop = ret.stop + stop
    #     ret = bot2.interact(Message(from_character=chr_bot.name,
    #                                 to_character=chr_me.name,
    #                                 action=ret.action,
    #                                 message=ret.message), chr_bot)
    #     stop = ret.stop + stop
    #
    #     if stop > 0:
    #         break
    #
    #     max_turn = max_turn - 1
    #
    # print(ret.dict())
