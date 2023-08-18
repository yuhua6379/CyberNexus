import os

from langchain.agents import OpenAIFunctionsAgent
from langchain.schema import SystemMessage

import initialize
from bot.base_bot import SimpleChatBot
from bot.toolkits.internet_tools.get_weather_information_in_china import get_weather_info_in_china
from bot.toolkits.system_tools.watch import watch
from bot.worker_bot import WorkerBot
from model.entities.message import Message
from model.llm import ChatGPT
from model.llm_broker import Character
from model.prompts.charlie_prompt_factory import CharliePromptFactory
from model.prompts.sample_prompt_factory import SamplePromptFactory
import tool_build_character

if __name__ == '__main__':
    # 初始化，一些数据库session和日志等公共组件
    initialize.initialize()
    tool_build_character.build()
    # print(f'your key is {os.environ["open_ai_key"]}')

    # 获取llm实例，用于后面predict
    llm = ChatGPT(model="gpt-3.5-turbo-0613")

    # 设置聊天对象，name是唯一的，会根据对象去加载历史聊天记录

    chr1 = Character.get_by_name("镇长")

    system_message = SystemMessage(content="")

    # 构建一个bot，用于聊天
    q = "帮我查询下贺州的天气"
    bot1 = WorkerBot(llm=llm, character=chr1, factory=CharliePromptFactory(), tools=[get_weather_info_in_china])
    r = bot1.do_something(q)
    print(q)
    print(r)
