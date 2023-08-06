from pydantic import BaseModel


class BaseSituation(BaseModel):
    step: int
    round: int
