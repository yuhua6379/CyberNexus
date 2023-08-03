import os

from bot.core import BotBuilder
from bot.prompt_factory.core import PromptFactory
from bot.prompt_factory.miser import miser_virtual_character
from bot.toolkits import get_weather_info_in_china
from bot.toolkits.system_tools import watch
from interact.command_line_interact import CommandLineInteracter
from interact.human_interact_with_bot import HumanInteractWithBot
from model.openai import get_openai_llm

if __name__ == '__main__':
    interact = HumanInteractWithBot(command_line=CommandLineInteracter())

    # 构造prompt，现在比较简陋，随便搞
    pb = PromptFactory(miser_virtual_character)
    print(pb.build())

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])
    bb = BotBuilder(llm=llm, tools=[get_weather_info_in_china, watch], prompt=str(pb))

    try:
        interact.start(bb)
    except CommandLineInteracter.StopException as e:
        print(e)
