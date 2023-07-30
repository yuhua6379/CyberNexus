import initialize
from bot.core import BotBuilder, Character
from bot.prompt_builder.core import PromptBuilder
from bot.prompt_builder.env_aware.level import Level
from bot.prompt_builder.env_aware.temperature import get_temperature_awareness
from bot.prompt_builder.env_aware.time_aware import get_time_awareness
from bot.toolkits.internet_tools.get_weather_information_in_china import get_weather_info_in_china
from bot.toolkits.system_tools.watch import watch
from datasource.rdbms.sqlite import CharacterModel, get_session
from model.openai import get_openai_llm
import os

try:
    with get_session() as session:
        me = CharacterModel()
        bot = CharacterModel()
        me.name = "yuhua"
        me.type = "user"
        bot.name = "bot"
        bot.type = "bot"
        session.add(me)
        session.add(bot)
        session.commit()
except Exception as e:
    pass


if __name__ == '__main__':
    initialize.initialize()
    print(f'your key is {os.environ["open_ai_key"]}')
    llm = get_openai_llm(openai_api_key=os.environ['open_ai_key'])

    me = Character.get_by_name("yuhua")
    bot = Character.get_by_name("bot")

    pb = PromptBuilder()
    pb.append(get_time_awareness(Level.weak))
    pb.append(get_temperature_awareness(Level.strong))
    agent = BotBuilder.build(character1=me, character2=bot, llm=llm, tools=[get_weather_info_in_china, watch], prompt=str(pb))
    agent.chat("我晚上8点的时候去逛街买了点东西，你记住，等下我会问你刚刚说了什么")
    agent.chat("还记得我刚刚跟你说了什么吗？")
    agent.chat("明明在记录里，你确定不记得？")




