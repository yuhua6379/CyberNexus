# BASE_PROMPT = '''
# []号之间代表的是角色的动作，例如:
# A: [奔跑着过来] 我很开心！
# B: [展开双臂迎接] 我也是，好久不见你了，我很挂念你
#
# A: [指着天空豪言壮语到] 我要成为世界第一的运动员
#
# {} 之间代表人物的外貌衣着等，例如:
# A: {带着帽子穿着外套} [抬头看着B] 你好高
# B: {身高8尺} [礼貌地说] 你好
# '''
BASE_PROMPT = ""

CONCLUDE_PROMPT_TEMPLATE = '''
下面有一段对话:
{history}
请你用一段长度适中的话总结一下这段对话，必须包含对话人物，而且你只能输出这句话
'''

# CHAT_TEMPLATE = '''{c1}对{c2}说: {content}'''
#
# ACTION_TEMPLATE = '''{c1}的行动: {content}'''

TOWARDS = "###>"
MESSAGE_TEMPLATE = '''{c1} '''+TOWARDS+''' {c2}: {action} |*| {message}'''

RELATIVE_MEMORY_TEMPLATE = '''以下是相关的一些记忆:\n{content}'''

RECENT_MEMORY_TEMPLATE = '''以下是最近的一些记忆:\n{content}'''

HISTORY_TEMPLATE = '''以下是你最近的对话:\n{content}'''

# LONG_TERM_PLAN_TEMPLATE = '''
# 现在，假设你是{c2}
# 请你做出回应
# '''

EMPTY_ACTION = "{无动作}"
EMPTY_MESSAGE = "{没说话}"
DELIMITER = "|*|"

REACT_FORMAT = f'''
对话消息必须符合以下格式：
这段消息与tools调用没有任何关系，
你使用符号"{TOWARDS}"表示消息发给某人
你回复的每一条消息用{DELIMITER}分割
并且你必须回复2条
第1条是角色做出的动作，不能包含'我'这种字眼，要用名字替代，如果角色不需要做动作，可以回复{EMPTY_ACTION}
第2条表示角色需要对某人说的话，或者自言自语，绝对不能用于陈述自己的行动，当不需要说话时可以回复{EMPTY_MESSAGE}
以下是回应示例:
例子:
lisa {TOWARDS} tom: lisa看了看天空，并对tom说道{DELIMITER}今天天气真不错，你不觉得吗？
'''

# 例子2:
# {
#    "action":"我看了看手表，加快了脚步前往教堂",
# }
# 例子3:
# {
#     "message":"这个真好吃！",
# }

REACT_TEMPLATE = '''
这是刚才的记录:
{c1} '''+TOWARDS+''' {c2}: {action} |*| {message}

现在，假设你是{c2}
请你做出回应
'''

NANE_OF_SYSTEM = "god"

MAX_SHORT_TERM_MEMORY = 10
