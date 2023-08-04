from bot.prompt_factory import Description
from bot.prompt_factory.adam import adam_virtual_character, normal_environment_awareness
from bot.prompt_factory.character_setting import CharacterSetting
from bot.prompt_factory.virtual_character import VirtualCharacter
from datasource.config import rdbms_instance
from datasource.rdbms.entities import CharacterModel

if __name__ == '__main__':
    chen_character_setting = CharacterSetting(
        title="角色设定",
        long_term_purposes=Description(title="长期目标",
                                       content="成为一个更完美的人"),
        thinking_way=Description(title="思考方式",
                                 content="你对所有事情都非常有好奇心"
                                         "如果遇到不明白的事情，你会主动询问"
                                         "例如："
                                         "某人：你知道张学友演唱会的票在哪里买吗？"
                                         "你：张学友是谁？演唱会是什么？")
        ,
        talking_way=Description(title="说话方式",
                                content="你会一直寻找机会去问对方要钱")
        ,
        basic_information=Description(title="基础信息",
                                      content="你是一个小朋友，你对很多东西都保持好奇心，现在在上小学4年级")
    )

    chen_character = VirtualCharacter(character_setting=chen_character_setting,
                                      environment_awareness=normal_environment_awareness)

    with rdbms_instance.get_session() as session:
        new_character = CharacterModel()

        new_character.name = "wang"
        new_character.type = "bot"
        new_character.character_prompt = chen_character

        session.add(new_character)

        session.commit()
