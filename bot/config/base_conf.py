HISTORY_FORMAT = '''
你可以理解角色之间的交互
你是构建json的能手，你可以精确地构建json
你必须用json格式表示角色的交互，如下：
from_character 代表发出动作或消息的角色
to_character 代表接受动作或消息的角色
action 此参数可选，含义是角色做出的动作，不能包含'我'这种字眼，要用名字替代，如果角色不需要做动作，可以不加入这个参数
message 此参数可选，含义是角色需要对某人说的话，或者自言自语，绝对不能用于陈述自己的行动，当不需要说话时，可以不加入这个参数
但是message和action至少有一个

例子：
{
    "from_character": "lisa",
    "to_character": "tom",
    "action": "lisa看了看天空，并对tom说道",
    "message": "今天天气真不错，你不觉得吗？"
}
'''

PLAN_FORMAT = '''
你可以理解角色的计划
你是构建json的能手，你可以精确地构建json
你必须用json格式表示角色的计划，如下：
plan是你的计划，是一个有顺序的数组，包含了若干个字符串，每一个字符串都是一个步骤
例如：
{"plan":["xxxx", "xxxxx"]}
'''

CONCLUDE_PROMPT_TEMPLATE = '''
''' + HISTORY_FORMAT + '''
这是最近的交互:
{history}

请你用一段长度适中的话总结一下这段交互，而且你只能输出这句话
'''

SHORT_TERM_PLAN_PROMPT_TEMPLATE = '''
''' + HISTORY_FORMAT + '''
这是最近的交互:
{history}

'''+PLAN_FORMAT+'''

这是你的长期计划:
{long_term_plan}

请你回应下一步该怎么做
'''

LONG_TERM_PLAN_PROMPT_TEMPLATE = '''
''' + HISTORY_FORMAT + '''
这是最近的交互:
{history}

'''+PLAN_FORMAT+'''

请你回应1个计划，包含{steps_of_round}个步骤
'''

RELATIVE_MEMORY_TEMPLATE = '''以下是相关的一些记忆:\n{content}'''

RECENT_MEMORY_TEMPLATE = '''以下是最近的一些记忆:\n{content}'''

HISTORY_TEMPLATE = '''以下是最近的交互:\n{content}'''


EMPTY_ACTION = ""
EMPTY_MESSAGE = ""

REACT_TEMPLATE = '''
这是刚才的记录:
{message}

现在，假设你是{c2}
请你做出回应
'''

NANE_OF_SYSTEM = "god"

MAX_SHORT_TERM_MEMORY = 10
