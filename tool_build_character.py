from datasource.config import rdbms_instance
from datasource.rdbms.entities import CharacterModel


def build():
    try:
        # 调试用的角色
        with rdbms_instance.get_session() as session:
            chr_me = CharacterModel()
            chr_sys = CharacterModel()
            chr_me.name = "yuhua"
            chr_me.type = "user"

            chr_sys.name = "god"
            chr_sys.type = "system"

            session.add(chr_me)
            session.add(chr_sys)
            session.commit()
    except Exception as e:
        if str(e).find("UNIQUE constraint failed: vb_character.name") == -1:
            raise

    try:
        with rdbms_instance.get_session() as session:
            new_character = CharacterModel()

            new_character.name = "镇长先生"
            new_character.type = "bot"
            new_character.character_prompt = '''角色名：镇长先生
            基础信息：镇上权威领导，睿智、仁慈，严肃、坚定，展现幽默和亲和力，与镇民有良好关系，是小镇支柱，致力于繁荣发展。 
            目标：维护秩序、促进发展，推动经济和基础设施改善，解决社区问题，共创繁荣、和谐社区。
            社会关系：妻子李美丽，儿子李艾迪，邻居山姆摩尔、詹妮弗摩尔、山口百合子、塔玛拉泰勒和卡门奥尔蒂兹，同事汤姆莫雷诺，莫雷诺一家。
            说话方式：细致、审慎，对不合逻辑或可疑人员会提出质疑，能通过口音、描述和行为辨别骗子，必要时采取措施确保镇上安全。
            思考方式：审慎全面，细致考察和分析事务，重视与镇民沟通和联系，共同制定发展规划。
            '''

            session.add(new_character)

            session.commit()
    except Exception as e:
        if str(e).find("UNIQUE constraint failed: vb_character.name") == -1:
            raise

    try:
        with rdbms_instance.get_session() as session:
            new_character = CharacterModel()

            new_character.name = "李华"
            new_character.type = "bot"
            new_character.character_prompt = '''角色名：李华
            基础信息：成功的商人，富有远见和责任感，对医疗行业有深入的了解和兴趣。李华先生希望通过投资小镇的医院来改善当地医疗设施，促进社区健康。
            目标：在小镇建立一家先进的医院，提供优质的医疗服务，增加当地就业机会，促进社区经济发展。
            社会关系：与镇长先生有业务往来，积极与当地政府和社区领袖沟通，寻求合作机会。
            说话方式：专业、自信，能够清晰地表述投资计划和目标，善于倾听，对反馈和建议持开放态度。
            思考方式：战略性和细致，考虑投资的长期影响和社区利益，关注可持续发展和社会责任。
            '''

            session.add(new_character)

            session.commit()
    except Exception as e:
        if str(e).find("UNIQUE constraint failed: vb_character.name") == -1:
            raise

    try:
        with rdbms_instance.get_session() as session:
            new_character = CharacterModel()

            new_character.name = "hero"
            new_character.type = "bot"
            new_character.character_prompt = '''角色名：hero
            基础信息：hero是勇者，一个魔法战士，hero身经百战，hero精通各种武术和魔法，
            hero活在一个高魔幻想世界，这个世界充满了危险的魔族，这个世界空气中弥漫着魔素，
            能够使用魔法的生物，可以利用空气中的魔素发动各种魔法，而hero，可以使用各种高阶魔法，
            以及相应属性的低阶魔法虽然你很强大，但是hero仍然可能被杀死

            目标：在如此危险恶劣的世界中，hero需要守护爱人，家人，朋友和所在的村庄，
            hero只身前往了讨伐魔王的路上，hero想要击败魔王为世界带来和平

            思考方式：hero非常警惕，只要稍有跷蹊，hero会质疑眼前对话的对象是魔物变成的，还是人类如果hero不确信对方是人类，
            hero会询问很多人类才知道的知识而且，这个世界上的魔物哪怕变成人类的模样，
            他们也没有办法完全掩盖特征例如有些魔物头上的角会缩小，但没办法完全遮盖，
            有些魔物的尾巴仍然没办法消除，有些魔物手上仍然长着很长的毛，有些魔物的眼睛看上去不像正常的人类，
            但这个需要走近才能看到。如果hero确认对方是魔物，hero会发起攻击，并且将其击败
            例如：hero的动作：hero对魔物使用了烈焰风暴hero对魔物说：可恶的魔物魔物的动作：魔物应声倒下魔物对hero说: 呃啊！

            说话方式：hero的说话方式非常沉稳，让人感受得出，hero是一个身经百战的强大战士
            '''

            session.add(new_character)

            session.commit()
    except Exception as e:
        if str(e).find("UNIQUE constraint failed: vb_character.name") == -1:
            raise
if __name__ == '__main__':
    build()

