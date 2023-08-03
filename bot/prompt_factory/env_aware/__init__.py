from pydantic import BaseModel

from bot.prompt_factory.env_aware.level import Level
from bot.prompt_factory.env_aware.temperature import get_temperature_awareness
from bot.prompt_factory.env_aware.time_aware import get_time_awareness


class EnvironmentAwareness(BaseModel):
    time_awareness: str
    temperature_awareness: str
