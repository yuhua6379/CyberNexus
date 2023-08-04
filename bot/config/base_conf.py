base_prompt = '''你是一个聪明的ai'''

conclude_prompt_template = '''
下面有一段对话:
{history}
请你用一句话总结一下这段对话，必须包含对话人物，而且你只能输出这句话
'''

sender_character_specify_template = '''现在假设我是{name}'''
recver_character_specify_template = '''现在假设你是{name}'''

title_of_relative_memory = '''以下是你最近的一些记忆'''

title_of_history = '''以下是你最近的对话'''

name_of_god = "god"

max_short_term_memory = 10
