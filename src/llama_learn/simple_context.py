from llama_index.core.workflow import Context
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent
import asyncio

agent = FunctionAgent(
    llm=OpenAI(model="gpt-4o-mini"),
    system_prompt="You are a helpful assistant.",
)


async def main():

    # create context
    ctx = Context(agent)

    # run agent with context
    response = await agent.run("My name is Logan", ctx=ctx)
    print(str(response))
    response = await agent.run("What is my name?", ctx=ctx)
    print(str(response))


if __name__ == "__main__":
    asyncio.run(main())
