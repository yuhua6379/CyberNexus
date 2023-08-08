# HISTORY_FORMAT = '''
# 你需要完成接下来的一系列对话，要求如下：
# 你必须用 JSON 格式表示角色之间的交互，具体要求如下：
# - "from_character": 代表发出动作或消息的角色。
# - "to_character": 代表接收动作或消息的角色。
# - "action": 此参数为可选，表示角色做出的动作。此处不能使用“我”，而应使用具体名字。若无动作，则不加入此参数。
# - "message": 此参数为可选，表示角色所说的话或者自言自语。不可用于陈述行动。若不需说话，则不加入此参数。
# - "message" 和 "action" 中至少要有一个。
# - "stop": 此参数意味着from_character代表的角色觉得对话已经结束，无需再进行回复。若无此参数，则默认为0，即对话未结束。
#
# 示例1：
# {
#     "from_character": "lisa",
#     "to_character": "tom",
#     "action": "看了看天空，并对 tom 说道",
#     "message": "今天天气真不错，你不觉得吗？",
#     "stop": 0
# }
#
# 示例2：
# {
#     "from_character": "tom",
#     "to_character": "jack",
#     "action": "一脸焦躁",
#     "message": "我必须走了，不然赶不上3点半的火车了",
#     "stop": 1
# }
#
# let's think step by step:
# 1. 生成一个json格式的对话；
# 2. 核实 json 格式，确保格式合法。
# 比如：{
#     "from_character": "hero",
#     "to_character": "镇长先生",
#     "action": "",
#     "message": "镇长先生，非常感谢您的关心和提醒。我明白保护社区和居民的重要性，这也是我前往讨伐魔王的初衷。我会尽我; pos=93; lineno=5; colno=16)
# 就不是一个合法的 json 格式。
# 3. 如果格式有问题，此时你需要重新生成正确的 json 格式。
#
# '''
#
# SCHEDULE_FORMAT = '''
# 你可以理解角色的schedule，使用以下格式:
# 你是构建json的能手，你可以精确地构建json，你在任何情况输出的都是json格式，且一定是可以解析的
# 你必须用json格式表示角色的计划，如下：
# schedule是你的日程，是一个有顺序的数组，包含了若干个字符串，每一个字符串都是一个步骤
# 例如：
# {
#     "schedule": ["xxxx", "xxxxx"]
# }
# '''
#
# CONCLUDE_PROMPT_TEMPLATE = '''
# {history_format}
# 这是最近的交互:
# {history}
#
# 请你用一段长度适中的话总结一下这段交互，而且你只能输出这句话
# '''
#
# IF_ITEM_DONE_TEMPLATE = '''
# 这是一些最近的记忆:
# {memory}
#
# 这是你计划做的事情，但这事情可能受到干扰未必会完成:
# {item}
#
# 这是最近的交互:
# {history_string}
#
# 请你用一句话总结一下你最近真正做的事情
# '''
#
# SCHEDULING_PROMPT_TEMPLATE = '''
# 这是一些最近的记忆:
# {memory}
#
# {schedule_format}
#
# 这是你已完成的事项:
# {item_done}
# 请你回应1个计划，包含{steps}个步骤
# '''
#
# RELATIVE_MEMORY_TEMPLATE = '''以下是相关的一些记忆:\n{content}'''
#
# RECENT_MEMORY_TEMPLATE = '''以下是最近的一些记忆:\n{content}'''
#
# HISTORY_TEMPLATE = '''以下是最近的交互:\n{content}'''
#
# EMPTY_ACTION = ""
# EMPTY_MESSAGE = ""
#
# REACT_TEMPLATE = '''
# 相关的记忆:
# {relative_memory}
#
# 最近的记忆:
# {recent_memory}
#
# 正在进行的计划:
# {item_doing}
#
# 交互记录：
# {history}
# 请生成{c2}的回复：<填写>
# '''
#
# NANE_OF_SYSTEM = "god"
#
# MAX_SHORT_TERM_MEMORY = 10
