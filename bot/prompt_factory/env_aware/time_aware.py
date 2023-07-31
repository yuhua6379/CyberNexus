from bot.prompt_factory.env_aware.level import Level

_strong_awareness = '''
you have a strong sense of time.
you must first confirm what day or what time it is before you do something.
once you forgot do the certain things, you will be very depressed.
'''

_weak_awareness = '''
you don't care about time and are often late or forget to do certain things.
when you forget what to do at this time, you will not give the correct feedback
'''

_normal_awareness = '''
your sense of time is similar to that of ordinary people, occasionally being late and forgetting to do certain things.
'''


def get_time_awareness(level: Level):
    if level.strong:
        return _strong_awareness
    elif level.weak:
        return _weak_awareness
    else:
        return _normal_awareness
