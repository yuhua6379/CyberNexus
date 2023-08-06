import os

import gradio as gr

import initialize
from bot.toolkits import get_weather_info_in_china
from bot.toolkits.system_tools import watch
from interact.human_interact_with_bot import HumanInteractWithBot
from model.openai import get_openai_llm
from repo.character import Character

if __name__ == '__main__':
    initialize.initialize()

    # 获取llm实例，用于后面predict
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])

    yuhua = Character.get_by_name('yuhua')
    fun = HumanInteractWithBot(llm,
                               [get_weather_info_in_china, watch],
                               human=yuhua)

    demo = gr.ChatInterface(fun)

    demo.launch()
