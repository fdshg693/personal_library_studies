import random

from google.adk.agents.llm_agent import Agent


def get_random_number(min_value: int = 1, max_value: int = 100) -> dict:
    """Returns a random integer between min_value and max_value (inclusive)."""
    number = random.randint(min_value, max_value)
    return {
        "status": "success",
        "min": min_value,
        "max": max_value,
        "number": number,
    }


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Returns a random number within a specified range.",
    instruction="You are a helpful assistant that returns random numbers. Use the 'get_random_number' tool to fetch a random integer, optionally within a user-specified range.",
    tools=[get_random_number],
)

from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Make your agent A2A-compatible
a2a_app = to_a2a(root_agent, port=8001)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(a2a_app, host="0.0.0.0", port=8001)
