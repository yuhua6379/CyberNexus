from bot.prompt_factory import Description, Prompt


class EnvironmentAwareness(Prompt):
    time_awareness: Description
    temperature_awareness: Description
