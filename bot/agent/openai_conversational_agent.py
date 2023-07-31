import logging
from typing import List, Tuple, Any, Union

from langchain.agents import OpenAIFunctionsAgent
from langchain.agents.openai_functions_agent.base import _format_intermediate_steps, _parse_ai_message
from langchain.callbacks.base import Callbacks
from langchain.schema import AgentAction, AgentFinish, HumanMessage, AIMessage

from bot.memory.shorterm_memory import History


class OpenAIConversationalAgent(OpenAIFunctionsAgent):
    # 具备记忆能力的OpenAi Agent，chat可以是对话形式

    @staticmethod
    def generate_messages_with_history(messages, kwargs):
        messages_with_history = []
        for history in kwargs["history"]:
            history: History
            human = HumanMessage(content=history.character1_message)
            ai = AIMessage(content=history.character2_message)
            messages_with_history.append(human)
            messages_with_history.append(ai)
        messages_with_history = [messages[0]] + messages_with_history + messages[1:]

        return messages_with_history

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
        messages = prompt.to_messages()

        # 原始的agent不带任何的history拼接，导致传递到openai底层没有聊天记录，所以openai agent没有记忆
        # 使用generate_messages_with_history可以为message加入history信息
        messages_with_history = self.generate_messages_with_history(messages, kwargs)

        prompt = prompt.dict()
        content = prompt["messages"][0]["content"]
        logging.debug(f"prompt: {content}\n\nfunctions: {self.functions}\n\nkwargs: {kwargs}\n\n")

        if with_functions:
            predicted_message = self.llm.predict_messages(
                messages_with_history,
                functions=self.functions,
                callbacks=callbacks,
            )
        else:
            predicted_message = self.llm.predict_messages(
                messages_with_history,
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

        agent_scratchpad = _format_intermediate_steps(intermediate_steps)
        selected_inputs = {
            k: kwargs[k] for k in self.prompt.input_variables if k != "agent_scratchpad"
        }
        full_inputs = dict(**selected_inputs, agent_scratchpad=agent_scratchpad)
        prompt = self.prompt.format_prompt(**full_inputs)
        messages = prompt.to_messages()

        # 原始的agent不带任何的history拼接，导致传递到openai底层没有聊天记录，所以openai agent没有记忆
        # 使用generate_messages_with_history可以为message加入history信息
        messages_with_history = self.generate_messages_with_history(messages, kwargs)

        predicted_message = await self.llm.apredict_messages(
            messages_with_history, functions=self.functions, callbacks=callbacks
        )
        agent_decision = _parse_ai_message(predicted_message)
        return agent_decision
