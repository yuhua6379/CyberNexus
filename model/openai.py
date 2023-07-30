from langchain.chat_models import ChatOpenAI


def get_openai_llm(openai_api_key: str) -> ChatOpenAI:
    return ChatOpenAI(openai_api_key=openai_api_key)