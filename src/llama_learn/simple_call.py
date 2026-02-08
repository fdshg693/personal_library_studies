from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI

llm = OpenAI(
    model="gpt-4o-mini",
    # api_key="some key",  # uses OPENAI_API_KEY env var by default
)


def test1():
    response = llm.complete("1+1= ")
    print(response)


def test2():
    messages = [
        ChatMessage(role="system", content="Your name is LlamaLearn."),
        ChatMessage(role="user", content="What is your name?"),
    ]

    chat_response = llm.chat(messages)
    print(chat_response)


if __name__ == "__main__":
    test1()
    test2()
