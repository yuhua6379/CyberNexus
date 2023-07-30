from langchain.agents import initialize_agent

import initialize
from bot.core import BotBuilder
from model.openai import get_openai_llm
from bot.toolkits import GetWeatherInformationInChina

import os
if __name__ == '__main__':
    initialize.initialize()
    print(f'your key is {os.environ["open_ai_key"]}')
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])
    agent = BotBuilder.build(llm=llm, tools=[GetWeatherInformationInChina()])
    print(agent.chat("我想知道现在广州的天气如何"))



