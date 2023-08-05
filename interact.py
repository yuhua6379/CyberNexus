import os

import initialize
from bot.core import Bot
from bot.toolkits import get_weather_info_in_china
from bot.toolkits.system_tools import watch
from interact.human_interact_with_bot import HumanInteractWithBot
from model.openai import get_openai_llm
from repo.character import Character
import random
import gradio as gr
if __name__ == '__main__':
    initialize.initialize()

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])

    yuhua = Character.get_by_name('yuhua')
    hero = Character.get_by_name('hero')
    fun = HumanInteractWithBot(llm,
                               [get_weather_info_in_china, watch],
                               human=yuhua,
                               bot=hero)

    demo = gr.ChatInterface(fun)

    demo.launch()
