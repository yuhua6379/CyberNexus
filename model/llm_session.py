import json
from abc import abstractmethod
from typing import Type, Optional, Callable, Any

from pydantic import BaseModel, ConfigDict

from common.base_thread import get_logger


class Context(BaseModel):
    # 正常情况下status必须为0，如果不为0，
    # 这个结果会跳过所有的回写和重试机制快速抛到最上层
    status: int = 0
    llm_output: Optional[str]
    _result: Optional[Any]
    result_type: Type

    @property
    def result(self):
        if issubclass(self.result_type, BaseModel):
            return self.result_type.parse_raw(self.llm_output)
        elif self.result_type == int:
            return int(self.llm_output)
        else:
            return self.llm_output

    def valid(self):
        _ = self.result

    def __str__(self):
        return f"status: {self.status} result: {self.result}"


class CallBack(Callable):
    """
    回调函数，可以处理LLM的原始返回值
    """

    def __call__(self, context: Context):
        self.call(context)

    @abstractmethod
    def call(self, context: Context):
        pass


class LLMSession:

    def __init__(self, prompt: str, result_type: Type, callback: Callable = None):
        self.prompt = prompt
        self.result_type = result_type
        self.context = Context(result_type=result_type)
        self.callback = callback

    def set_result(self, result):
        self.context.llm_output = result
        if self.callback is not None:
            self.callback(self.context)

    def get_prompt(self):
        return self.prompt

    def get_context(self):
        return self.context


def pydantic2prompt(type_: Type[BaseModel], title, examples: list[BaseModel] = (),
                    example_title=None):
    schema = type_.schema()
    s = [title]
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
    # 回调函数
    callback: Optional[Any]

    @classmethod
    def beautify_prompt(cls, prompt_template, kwargs: dict):
        s = []
        for item in prompt_template.split("\n"):
            s.append(item.strip())
        prompt_template = "\n".join(s)

        # 不允许中文逗号
        prompt_template.replace("，", ",")

        for k, v in kwargs.items():
            s = []
            v_list = str(v).split("\n")
            if len(v_list) > 1:
                # 太简单的值不予处理
                for item in v_list:
                    s.append("\t" + item.strip())
                kwargs[k] = "\n".join(s)

            kwargs[k] = str(kwargs[k]).replace('，', ',')
        return prompt_template, kwargs


def build_prompt_event(type_: Type, title=None, example_title=None, examples: list = ()):
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
        def wrapper(self, *args, **kwargs) -> LLMSession:
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

            return LLMSession(prompt=prompt, result_type=type_, callback=ret.callback)

        return wrapper

    return decorator


def build_prompt_phase(func):
    def wrapper(self, *args, **kwargs) -> str:
        # 适配所有成员函数的wrapper

        ret: PromptReturn = func(self, *args, **kwargs)
        prompt_template, kwargs = ret.prompt_template, ret.kwargs

        prompt_template, kwargs = PromptReturn.beautify_prompt(prompt_template, kwargs)
        prompt = prompt_template.format(**kwargs)
        get_logger().debug(f"{func.__name__}: \n{prompt}")

        return prompt

    return wrapper
