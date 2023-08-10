from pydantic import BaseModel, Field


class Schedule(BaseModel):
    schedule: list[str] = Field(description="代表日程，是一个有顺序的数组，包含了若干个字符串，每一个字符串都是一个步骤")

    def to_prompt(self):
        ret = ""
        for idx, step in enumerate(self.schedule):
            ret += f"{idx + 1}.{step}"
        if len(ret) == 0:
            ret = ""
        return ret
