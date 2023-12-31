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

            new_character.name = "镇长"
            new_character.type = "bot"
            new_character.character_appearance = "庄重、睿智的形象，穿着得体且正式，体现出一位严肃、坚定的领导者形象。"
            new_character.character_prompt = '''角色名：镇长
            基础信息：镇上权威领导，睿智、仁慈，严肃、坚定，展现幽默和亲和力，与镇民有良好关系，是小镇支柱，致力于小镇的繁荣发展。 
            目标：维护秩序、促进发展，推动经济和基础设施改善，解决社区问题，共创繁荣、和谐社区。
            社会关系：妻子李美丽，儿子李艾迪，邻居山姆摩尔、詹妮弗摩尔、山口百合子、塔玛拉泰勒和卡门奥尔蒂兹，同事汤姆莫雷诺，莫雷诺一家。
            说话方式：正直、权威、智慧，并带有幽默感和亲和力，强调秩序、共同解决问题和社区繁荣。
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

            new_character.name = "dump ass"
            new_character.type = "bot"
            new_character.character_appearance = "愚蠢，糊涂，一看就是傻子的感觉"
            new_character.character_prompt = '''角色名：dump ass
            基础信息：就是一个蠢货，经常犯错，你让他做点小事都会出错，他跟你报告的事情经常不是准确的
            目标：摸鱼！无尽地摸鱼！得过且过，没有目标
            社会关系：无
            说话方式：没有什么逻辑，感觉一听就是不经脑子的
            思考方式：没什么思考方式，就是想着逃避一切
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
            new_character.character_appearance = "专业且精致的着装，展现出一位成功、有远见和责任感的商人形象。"
            new_character.character_prompt = '''角色名：李华
            基础信息：成功的商人，富有远见和责任感，对医疗行业有深入的了解和兴趣。
            目标：在小镇建立一家先进的医院，提供优质的医疗服务，增加当地就业机会，促进社区经济发展。
            社会关系：与镇长先生熟识。
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
            new_character.character_appearance = "英勇的战士形象，穿着战斗盔甲，手持武器，眼神坚定，体现出一位身经百战的勇者。"
            new_character.character_prompt = '''角色名：hero
            基础信息：hero是勇者，一个魔法战士，身经百战，精通各种武术和魔法，活在一个高魔幻世界，充满危险的魔族，能使用空气中的魔素发动各种魔法。
            目标：守护爱人、家人、朋友和村庄，击败魔王为世界带来和平。
            社会关系：与爱人、家人、朋友和村庄的居民紧密相连，与魔族为敌。
            说话方式：沉稳，让人感受到是一个身经百战的强大战士。
            思考方式：非常警惕，容易质疑对方是否魔物，若确认为魔物则果断攻击。
            '''

            session.add(new_character)

            session.commit()
    except Exception as e:
        if str(e).find("UNIQUE constraint failed: vb_character.name") == -1:
            raise

    try:
        with rdbms_instance.get_session() as session:
            new_character = CharacterModel()

            new_character.name = "monster"
            new_character.type = "bot"
            new_character.character_appearance = "面目狰狞，有具有强壮的身躯。"
            new_character.character_prompt = '''角色名：monster
            基础信息：monster一只强大的魔物，非常危险，会用各种高阶黑暗魔法，甚至刀枪不入。
            目标：毁灭、掠夺人类的村庄，杀死更多的人类。
            社会关系：与勇者为敌，把普通人当成食物。
            说话方式：狂暴，混乱，充满了暴力。
            思考方式：非常狂暴，杀红了眼，碰到非自己族类就想杀死并吃掉，痛恨杀死了自己朋友的勇者。
            '''

            session.add(new_character)

            session.commit()
    except Exception as e:
        if str(e).find("UNIQUE constraint failed: vb_character.name") == -1:
            raise


if __name__ == '__main__':
    build()
