import os

import initialize
from bot.core import BotBuilder, Character
from bot.prompt_factory.core import PromptFactory
from bot.prompt_factory.env_aware.level import Level
from bot.prompt_factory.env_aware.temperature import get_temperature_awareness
from bot.prompt_factory.env_aware.time_aware import get_time_awareness
from bot.prompt_factory.miser import miser_virtual_character
from bot.toolkits.internet_tools.get_weather_information_in_china import get_weather_info_in_china
from bot.toolkits.system_tools.watch import watch
from datasource.rdbms.sqlite import CharacterModel, get_session
from model.openai import get_openai_llm

try:
    with get_session() as session:
        chr_me = CharacterModel()
        chr_bot = CharacterModel()
        chr_me.name = "yuhua"
        chr_me.type = "user"
        chr_bot.name = "bot"
        chr_bot.type = "bot"
        session.add(chr_me)
        session.add(chr_bot)
        session.commit()
except Exception as e:
    pass

if __name__ == '__main__':
    # 初始化，一些数据库session和日志等公共组件
    initialize.initialize()
    print(f'your key is {os.environ["open_ai_key"]}')

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录
    chr_me = Character.get_by_name("yuhua")
    chr_bot = Character.get_by_name("bot")

    # 构造prompt，现在比较简陋，随便搞
    pb = PromptFactory(miser_virtual_character)
    print(pb.build())

    # 构建一个bot，用于聊天
    bot = BotBuilder.build(character1=chr_me, character2=chr_bot, llm=llm, tools=[get_weather_info_in_china, watch],
                           prompt=str(pb))
    bot.chat("今天纽约热吗？")
