import initialize
import tool_build_character
from bot.base_bot import SimpleChatBot
from model.llm import ChatGPT
from model.llm_broker import Character
from model.prompts.charlie_prompt_factory import CharliePromptFactory
from world.botbroker import SyncBotBroker
from world.world import SimpleTuneBaseWorld

tool_build_character.build()

if __name__ == '__main__':
    # 初始化，一些数据库session和日志等公共组件
    initialize.initialize()
    # print(f'your key is {os.environ["open_ai_key"]}')

    # 获取llm实例，用于后面predict
    llm = ChatGPT(model="gpt-3.5-turbo-0613")

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录

    chr1 = Character.get_by_name("镇长")
    chr2 = Character.get_by_name("李华")

    # 构建一个bot，用于聊天
    bot1 = SimpleChatBot(llm=llm, character=chr1, factory=CharliePromptFactory())
    bot2 = SimpleChatBot(llm=llm, character=chr2, factory=CharliePromptFactory())

    world = SimpleTuneBaseWorld(steps_of_round=2, broker=SyncBotBroker())
    world.join(bot1)
    world.join(bot2)

    max_turn = 4
    for i in range(max_turn):

        # 一回合开始
        ret1 = bot1.meet(chr2)
        if ret1.status != 0:
            print(f"{chr1.name}没有与{chr2.name}互动")
        ret2 = bot2.interact(ret1.result)

        print(ret1.result.to_prompt())
        print(ret2.result.to_prompt())

        while True:
            if ret1.result.stop + ret2.result.stop > 0:
                print("对话结束")
                break
            ret1 = bot1.interact(ret2.result)

            ret2 = bot2.interact(ret1.result)

            print(ret1.result.to_prompt())
            print(ret2.result.to_prompt())

        # 互相生成印象
        bot1.make_impression(chr2)
        bot2.make_impression(chr1)

        bot1.conclude_interactions()
        bot2.conclude_interactions()

        # 跑到下一个round位置
        world.run_until_next_round()
