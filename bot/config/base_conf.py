# HISTORY_FORMAT = '''
# 你可以理解角色之间的交互，当且仅当需要理解角色交互时，使用以下格式:
# 你是构建json的能手，你可以精确地构建json，你在任何情况输出的都是json格式，且一定是可以解析的
# 你必须用json格式表示角色的交互，如下：
# from_character 代表发出动作或消息的角色
# to_character 代表接受动作或消息的角色
# action 此参数可选，含义是角色做出的动作，不能包含'我'这种字眼，要用名字替代，如果角色不需要做动作，可以不加入这个参数
# message 此参数可选，含义是角色需要对某人说的话，或者自言自语，绝对不能用于陈述自己的行动，当不需要说话时，可以不加入这个参数
# 但是message和action至少有一个
#
# 例子：
# {
#     "from_character": "lisa",
#     "to_character": "tom",
#     "action": "lisa看了看天空，并对tom说道",
#     "message": "今天天气真不错，你不觉得吗？"
# }
# '''

HISTORY_FORMAT = '''
你需要完成接下来的一系列对话，要求如下：
"""
你必须用 JSON 格式表示角色之间的交互，具体如下：
- "from_character": 代表发出动作或消息的角色。
- "to_character": 代表接收动作或消息的角色。
- "action": 此参数为可选，表示角色做出的动作。此处不能使用‘我’，而应使用具体名字。若无动作，则不加入此参数。
- "message": 此参数为可选，表示角色所说的话或者自言自语。不可用于陈述行动。若不需说话，则不加入此参数。
- "message" 和 "action" 中至少要有一个。

示例：
{
    "from_character": "lisa",
    "to_character": "tom",
    "action": "lisa 看了看天空，并对 tom 说道 ",
    "message": " 今天天气真不错，你不觉得吗？"
}
"""
'''

PLAN_FORMAT = '''
你可以理解角色的计划，当且仅当需要理解角色计划时，使用以下格式:
你是构建json的能手，你可以精确地构建json，你在任何情况输出的都是json格式，且一定是可以解析的
你必须用json格式表示角色的计划，如下：
plan是你的计划，是一个有顺序的数组，包含了若干个字符串，每一个字符串都是一个步骤
例如：
{"plan":["xxxx", "xxxxx"]}
'''

CONCLUDE_PROMPT_TEMPLATE = '''
{history_format}
这是最近的交互:
{history}

请你用一段长度适中的话总结一下这段交互，而且你只能输出这句话
'''

SHORT_TERM_PLAN_PROMPT_TEMPLATE = '''
这是一些最近的记忆:
{memory}

{plan_format}
这是你的长期计划:
{long_term_plan}

这是你最近执行了的计划，可能处于某些原因实际执行的结果会跟你的长期计划有冲突，以执行了的计划为准:
{executed_plan}

请你回应1个计划，包含1个步骤，记住，仅仅只有1个步骤
'''

LONG_TERM_PLAN_PROMPT_TEMPLATE = '''
这是一些最近的记忆:
{memory}

{plan_format}
请你回应1个计划，包含{steps_of_round}个步骤
'''

RELATIVE_MEMORY_TEMPLATE = '''以下是相关的一些记忆:\n{content}'''

RECENT_MEMORY_TEMPLATE = '''以下是最近的一些记忆:\n{content}'''

HISTORY_TEMPLATE = '''以下是最近的交互:\n{content}'''


EMPTY_ACTION = ""
EMPTY_MESSAGE = ""

# REACT_TEMPLATE = '''
# 这是刚才的记录:
# {message}
#
# 现在，假设你是{c2}
# 请你做出回应
# '''
REACT_TEMPLATE = '''
对话记录：
{message}
你的回复：<填写>
'''

NANE_OF_SYSTEM = "god"

MAX_SHORT_TERM_MEMORY = 10
