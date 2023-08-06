from datasource.config import rdbms_instance
from datasource.rdbms.entities import CharacterModel
from prompt.prompt_factory import Description
from prompt.prompt_factory.adam import normal_environment_awareness
from prompt.prompt_factory.character_setting import CharacterSetting
from prompt.prompt_factory.virtual_character import VirtualCharacter

if __name__ == '__main__':
    # chen_character_setting = CharacterSetting(
    #     title="角色设定",
    #     long_term_purposes=Description(title="hero的长期目标",
    #                                    content="在如此危险恶劣的世界中，hero需要守护爱人，家人，朋友和所在的村庄，hero只身前往了讨伐魔王的路上，hero想要击败魔王为世界带来和平"),
    #     thinking_way=Description(title="hero的思考方式",
    #                              content="hero非常警惕，只要稍有跷蹊，hero会质疑眼前对话的对象是魔物变成的，还是人类"
    #                                      "如果hero不确信对方是人类，hero会询问很多人类才知道的知识"
    #                                      "而且，这个世界上的魔物哪怕变成人类的模样，他们也没有办法完全掩盖特征"
    #                                      "例如有些魔物头上的角会缩小，但没办法完全遮盖，"
    #                                      "有些魔物的尾巴仍然没办法消除，"
    #                                      "有些魔物手上仍然长着很长的毛，"
    #                                      "有些魔物的眼睛看上去不像正常的人类，但这个需要走进才能看到。"
    #                                      "如果hero确认对方是魔物，hero会发起攻击，并且将其击败"
    #                                      "例如："
    #                                      "hero的动作：hero对魔物使用了烈焰风暴"
    #                                      "hero对魔物说：可恶的魔物"
    #                                      "魔物的动作：魔物应声倒下"
    #                                      "魔物对hero说: 呃啊！")
    #     ,
    #     talking_way=Description(title="说话方式",
    #                             content="hero的说话方式非常沉稳，让人感受得出，hero是一个身经百战的强大战士")
    #     ,
    #     basic_information=Description(title="hero的基础信息",
    #                                   content="hero是勇者，一个魔法战士，hero身经百战，"
    #                                           "hero精通各种武术和魔法，hero活在一个高魔幻想世界，"
    #                                           "这个世界充满了危险的魔族，这个世界空气中弥漫着魔素，"
    #                                           "能够使用魔法的生物，可以利用空气中的魔素发动各种魔法，"
    #                                           "而hero，可以使用各种高阶魔法，以及相应属性的低阶魔法"
    #                                           "虽然你很强大，但是你仍然可能被杀死")
    # )
    #
    # chen_character = VirtualCharacter(character_setting=chen_character_setting,
    #                                   environment_awareness=normal_environment_awareness)

    with rdbms_instance.get_session() as session:
        new_character = CharacterModel()

        new_character.name = "镇长先生"
        new_character.type = "bot"
        new_character.character_prompt = '''
        角色镇长先生信息如下：
"""
名字：镇长先生
基础信息：镇长先生，是镇上的权威领导者，他通常是一个睿智而仁慈的人物。镇长先生经常以严肃和坚定的态度处理问题，但也时常展现出幽默和亲和力，与镇民们建立了良好的关系。镇民的忠诚领袖和奋斗伙伴。他是这个小镇的支柱，镇长先生与镇民们一起他经常召开镇民大会，倾听居民的声音，并与他们共同制定发展规划。在这个和谐宁静的环境里，镇长先生是大家的指路明灯，为小镇的繁荣发展贡献着自己的力量。
目标：负责维护秩序、促进发展，并为居民提供指导和帮助。致力于推动经济发展、改善基础设施，并解决各种社区问题。共同创造一个繁荣、和谐的社区。

"""
        '''

        session.add(new_character)

        session.commit()
