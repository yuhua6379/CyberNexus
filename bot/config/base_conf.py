base_prompt = '''
[]号之间代表的是角色的动作，例如:
A: [奔跑着过来] 我很开心！
B: [展开双臂迎接] 我也是，好久不见你了，我很挂念你

A: [指着天空豪言壮语到] 我要成为世界第一的运动员

{} 之间代表人物的外貌衣着等，例如:
A: {带着帽子穿着外套} [抬头看着B] 你好高
B: {身高8尺} [礼貌地说] 你好

'''

conclude_prompt_template = '''
下面有一段对话:
{history}
请你用一段长度适中的话总结一下这段对话，必须包含对话人物，而且你只能输出这句话
'''

sender_character_specify_template = '''现在假设我是{name}'''
recver_character_specify_template = '''现在假设你是{name}'''

title_of_relative_memory = '''以下是你最近的一些记忆'''

title_of_history = '''以下是你最近的对话'''

name_of_god = "god"

max_short_term_memory = 10
