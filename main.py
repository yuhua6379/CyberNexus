import os

import initialize
from bot.core import Character, Bot
from bot.prompt_factory.adam import adam_virtual_character
from bot.toolkits.internet_tools.get_weather_information_in_china import get_weather_info_in_china
from bot.toolkits.system_tools.watch import watch
from datasource.config import rdbms_instance
from datasource.rdbms.entities import CharacterModel
from model.openai import get_openai_llm

if __name__ == '__main__':
    # 初始化，一些数据库session和日志等公共组件
    initialize.initialize()
    # print(f'your key is {os.environ["open_ai_key"]}')

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录
    chr_me = Character.get_by_name("yuhua")
    chr_bot = Character.get_by_name("adam")

    # 构建一个bot，用于聊天
    bot = Bot(llm=llm, tools=[get_weather_info_in_china, watch], character=chr_bot)
    bot.interact("我刚刚说了啥", chr_me)
