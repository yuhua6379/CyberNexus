from pydantic import BaseModel

from prompt.prompt_factory.character_setting import CharacterSetting
from prompt.prompt_factory.env_aware import EnvironmentAwareness


class VirtualCharacter(BaseModel):
    character_setting: CharacterSetting
    environment_awareness: EnvironmentAwareness
