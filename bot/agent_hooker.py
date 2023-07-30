import logging
from typing import List, Tuple, Any, Union

from langchain.agents import OpenAIFunctionsAgent as OriginOpenAIFunctionsAgent
from langchain.agents.openai_functions_agent.base import _format_intermediate_steps
from langchain.callbacks.base import Callbacks
from langchain.schema import AgentAction, AgentFinish


class OpenAIFunctionsAgent(OriginOpenAIFunctionsAgent):

    def plan(
            self,
            intermediate_steps: List[Tuple[AgentAction, str]],
            callbacks: Callbacks = None,
            with_functions: bool = True,
            **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        agent_scratchpad = _format_intermediate_steps(intermediate_steps)
        selected_inputs = {
            k: kwargs[k] for k in self.prompt.input_variables if k != "agent_scratchpad"
        }
        full_inputs = dict(**selected_inputs, agent_scratchpad=agent_scratchpad)
        prompt = self.prompt.format_prompt(**full_inputs)
        prompt = prompt.dict()
        content = prompt["messages"][0]["content"]
        logging.info(f"prompt: {content}\n\nfunctions: {self.functions}\n\nkwargs: {kwargs}\n\n")
        return super().plan(intermediate_steps,
                            callbacks,
                            with_functions,
                            **kwargs)
