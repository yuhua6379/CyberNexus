import json
from typing import Type, Optional

from pydantic import BaseModel

from common.base_thread import get_logger


class LLMSession:
    def __init__(self, prompt: str, result_type: Type):
        self.prompt = prompt
        self.result_type = result_type
        self.result = None

    def set_result(self, result):
        self.result = result

    def get_prompt(self):
        return self.prompt

    def get_result(self):
        if issubclass(self.result_type, BaseModel):
            return self.result_type.parse_raw(self.result)
        else:
            return self.result

    def __str__(self):
        return str(self.get_result())


def pydantic2prompt(type_: Type[BaseModel], title, examples: list[BaseModel] = (),
                    example_title=None):
    schema = type_.schema()
    s = list()
    s.append(title)
    for key, p in schema["properties"].items():
        s.append(f"\t- {key}: {p['description']}")

    s.append("\n")
    if example_title is not None:
        s.append(example_title)
    for n, sample in enumerate(examples):
        sample = json.dumps(sample.dict(), ensure_ascii=False)
        s.append(f"\t例子{n}: {sample}")

    return "\n".join(s)


class PromptReturn(BaseModel):
    # prompt模板
    prompt_template: str
    # 模板参数，除了return_type标记的返回类型
    kwargs: dict
    # 返回类型的描述放的位置
    position: Optional[str]

    @classmethod
    def beautify_prompt(cls, prompt_template, kwargs: dict):
        s = []
        for item in prompt_template.split("\n"):
            s.append(item.strip())
        prompt_template = "\n".join(s)

        for k, v in kwargs.items():
            s = []
            for item in str(v).split("\n"):
                s.append("\t" + item.strip())
            kwargs[k] = "\n".join(s)
        return prompt_template, kwargs


def return_type(type_: Type, title=None, example_title=None, examples: list = ()):
    """
    注册返回类型，返回类型生成的prompt会在prompt在模板指定位置
    具体指定方法，需要返回一个tuple，
    第一个是prompt_template
    第二个是position
    """
    if not issubclass(type_, BaseModel):
        if type_ not in [str, int]:
            raise RuntimeError("only support int,str,pydantic")

    def decorator(func):
        # 输入函数
        def wrapper(self, *args, **kwargs):
            # 适配所有成员函数的wrapper

            ret: PromptReturn = func(self, *args, **kwargs)
            prompt_template, kwargs, position = ret.prompt_template, ret.kwargs, ret.position

            if issubclass(type_, BaseModel) and position is not None:
                # 特殊类型生成的prompt在position处
                prompt_return = pydantic2prompt(type_, title, examples, example_title)
                kwargs[position] = prompt_return

            prompt_template, kwargs = PromptReturn.beautify_prompt(prompt_template, kwargs)
            prompt = prompt_template.format(**kwargs)
            get_logger().debug(f"{func.__name__}: \n{prompt}")

            return LLMSession(prompt=prompt, result_type=type_)

        return wrapper

    return decorator
