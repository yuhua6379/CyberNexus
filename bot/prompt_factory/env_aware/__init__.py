
from bot.prompt_factory import Description, BasePrompt, Prompt


class EnvironmentAwareness(Prompt):
    time_awareness: Description
    temperature_awareness: Description
