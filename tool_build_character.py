from bot.prompt_factory.adam import adam_virtual_character
from datasource.config import rdbms_instance
from datasource.rdbms.entities import CharacterModel

if __name__ == '__main__':
    with rdbms_instance.get_session() as session:
        new_character = CharacterModel()

        new_character.name = "adam"
        new_character.type = "bot"
        new_character.character_prompt = adam_virtual_character

        session.add(new_character)

        session.commit()
