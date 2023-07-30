import initialize
from bot.core import BotBuilder
from bot.prompt_builder.core import PromptBuilder
from bot.prompt_builder.env_aware.level import Level
from bot.prompt_builder.env_aware.temperature import get_temperature_awareness
from bot.prompt_builder.env_aware.time_aware import get_time_awareness
from bot.toolkits.system_tools.watch import Watch
from model.openai import get_openai_llm
from bot.toolkits import GetWeatherInformationInChina

import os
if __name__ == '__main__':
    initialize.initialize()
    print(f'your key is {os.environ["open_ai_key"]}')
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])

    pb = PromptBuilder()
    pb.append(get_time_awareness(Level.strong))
    pb.append(get_temperature_awareness(Level.strong))
    agent = BotBuilder.build(llm=llm, tools=[GetWeatherInformationInChina(), Watch()], prompt=str(pb))
    print(agent.chat("你应该还记得你答应我，下午2点前帮我去买张机票吧？现在买到了吗？"))



