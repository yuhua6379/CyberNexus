from langchain.agents import initialize_agent

import initialize
from agent.core import AgentBuilder
from model.openai import get_openai_llm
from agent.toolkits import GetWeatherInformationInChina
if __name__ == '__main__':
    initialize.initialize()
    llm = get_openai_llm(openai_api_key='')
    agent = AgentBuilder.build(llm=llm, tools=[GetWeatherInformationInChina()])
    agent.run("我想知道现在澳洲堪培拉的天气如何")



