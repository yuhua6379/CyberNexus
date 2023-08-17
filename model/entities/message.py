from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Message(BaseModel):
    from_character: str = Field(description="代表发出动作或消息的角色。")

    to_character: str = Field(description="代表接收动作或消息的角色。")

    action: Optional[str] = Field(description="此参数为可选，表示角色做出的动作。"
                                              "此处不能使用“我”，而应使用具体名字。"
                                              "若无动作，则不加入此参数。"
                                              "message 和 action 中至少要有一个。")

    message: Optional[str] = Field(description="此参数为可选，表示角色所说的话或者自言自语。"
                                               "不可用于陈述行动。若不需说话，则不加入此参数。message不能超过50字"
                                               "message 和 action 中至少要有一个。")

    stop: int = Field(description="此参数意味着from_character代表的角色觉得对话已经结束(2 of 10)，无需再进行回复。"
                                  "若无此参数，则默认为0，即对话未结束。", default=0)

    def to_prompt(self, simple_string=False):
        if simple_string:
            return f'{self.from_character}的动作:{self.action}\n{self.from_character}对{self.to_character}说:{self.message}'
        import json
        return json.dumps(self.dict(), ensure_ascii=False)
