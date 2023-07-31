import logging
from typing import List, Tuple, Any, Union

from langchain.agents import OpenAIFunctionsAgent as OriginOpenAIFunctionsAgent
from langchain.agents.openai_functions_agent.base import _format_intermediate_steps, _parse_ai_message
from langchain.callbacks.base import Callbacks
from langchain.schema import AgentAction, AgentFinish, HumanMessage, AIMessage

from bot.memory.shorterm_memory import ShortTermMemory


class OpenAIFunctionsAgent(OriginOpenAIFunctionsAgent):

    def plan(
            self,
            intermediate_steps: List[Tuple[AgentAction, str]],
            callbacks: Callbacks = None,
            with_functions: bool = True,
            **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date, along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        agent_scratchpad = _format_intermediate_steps(intermediate_steps)
        selected_inputs = {
            k: kwargs[k] for k in self.prompt.input_variables if k != "agent_scratchpad"
        }
        full_inputs = dict(**selected_inputs, agent_scratchpad=agent_scratchpad)
        prompt = self.prompt.format_prompt(**full_inputs)
        messages = prompt.to_messages()
        message_with_history = [messages[0]]
        for history in kwargs["history"]:
            history: ShortTermMemory
            human = HumanMessage(content=history.character1_message)
            ai = AIMessage(content=history.character2_message)
            message_with_history.append(human)
            message_with_history.append(ai)

        prompt = prompt.dict()
        content = prompt["messages"][0]["content"]
        logging.debug(f"prompt: {content}\n\nfunctions: {self.functions}\n\nkwargs: {kwargs}\n\n")

        if with_functions:
            predicted_message = self.llm.predict_messages(
                message_with_history,
                functions=self.functions,
                callbacks=callbacks,
            )
        else:
            predicted_message = self.llm.predict_messages(
                messages,
                callbacks=callbacks,
            )
        agent_decision = _parse_ai_message(predicted_message)
        return agent_decision

    async def aplan(
            self,
            intermediate_steps: List[Tuple[AgentAction, str]],
            callbacks: Callbacks = None,
            **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        agent_scratchpad = _format_intermediate_steps(intermediate_steps)
        selected_inputs = {
            k: kwargs[k] for k in self.prompt.input_variables if k != "agent_scratchpad"
        }
        full_inputs = dict(**selected_inputs, agent_scratchpad=agent_scratchpad)
        prompt = self.prompt.format_prompt(**full_inputs)
        messages = prompt.to_messages()
        predicted_message = await self.llm.apredict_messages(
            messages, functions=self.functions, callbacks=callbacks
        )
        agent_decision = _parse_ai_message(predicted_message)
        return agent_decision
