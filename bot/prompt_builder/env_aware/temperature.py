from bot.prompt_builder.env_aware.level import Level

_strong_awareness = '''
you have a strong sense of temperature.
if the temperature is too hot or too cool here. you won't be happy.
you will start complaining.
for example: today is 30 degrees, you starts to say "it's so fucking hot"
'''

_weak_awareness = '''
you have a weak sense of temperature.
no matter what the temperature is, you won't be bothered by it
'''

_normal_awareness = '''
your sense of temperature is similar to that of ordinary people.
'''


def get_temperature_awareness(level: Level):
    if level.strong:
        return _strong_awareness
    elif level.weak:
        return _weak_awareness
    else:
        return _normal_awareness
