from typing import List, Optional
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.tools import BaseTool
from pydantic import BaseModel
from langchain.chat_models.base import BaseChatModel
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from agent.config.base_prompt import get_base_prompt


class AgentBuilder(BaseModel):
    llm: BaseChatModel
    tools: List[BaseTool]
    prompt: str

    @staticmethod
    def build(llm: BaseChatModel, tools: List[BaseTool], prompt: Optional[str] = None) -> AgentExecutor:
        if prompt is None:
            prompt = get_base_prompt()
        if isinstance(llm, ChatOpenAI):
            system_message = SystemMessage(
                content=prompt)
            prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
            agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
            return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
        else:
            raise Exception(f"unknown llm type: {type(llm)}")
