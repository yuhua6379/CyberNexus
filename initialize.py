from common.log import logger
from datasource.config import rdbms_instance
from datasource.rdbms.entities import CharacterModel
from prompt.prompt_factory.adam import adam_virtual_character


def initialize():
    logger.initialize()

    try:
        with rdbms_instance.get_session() as session:
            chr_me = CharacterModel()
            chr_bot = CharacterModel()
            chr_sys = CharacterModel()
            chr_me.name = "yuhua"
            chr_me.type = "user"

            chr_bot.name = "adam"
            chr_bot.type = "bot"
            chr_bot.character_prompt = ""#adam_virtual_character

            chr_sys.name = "god"
            chr_sys.type = "system"

            session.add(chr_me)
            session.add(chr_bot)
            session.add(chr_sys)
            session.commit()
    except Exception as e:
        if str(e).find("UNIQUE constraint failed: vb_character.name") == -1:
            raise
