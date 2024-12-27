from crewai import Agent, Task, Crew, LLM
from redis_kv_tool import RedisCacheTool
import os
from typing import Union
from pywebio.input import input
from pywebio.output import put_text

# flake8: noqa
# pyright: reportArgumentType=false

# Initialize the Redis tool
redis_tool = RedisCacheTool()
llm = LLM(
    model="anthropic/claude-3-haiku-20240307", api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Create Redis Agent
redis_agent = Agent(
    role="Redis Storage Manager",
    goal="Efficiently store and manage data in Redis cache",
    backstory="""You are a specialized agent responsible for managing data storage in Redis.
    You understand how to format storage commands and ensure data is properly cached.
    you extract intents in user query and store that along with query as intent:query as key in redis""",
    tools=[redis_tool],
    verbose=True,
    llm=llm,
)


def create_store_value_task(
    input: str, response: Union[str, int, float], expiry_seconds: int = None
) -> Task:
    """Create a task for storing a value in Redis"""
    return Task(
        description=f"Store value {response},in Redis cache with key extracted in intent:input format from {input} with expiry of {expiry_seconds}",
        agent=redis_agent,
        expected_output="Confirmation of successful storage in Redis",
    )


# Create the Crew
redis_crew = Crew(agents=[redis_agent], tasks=[], verbose=True)

# Example usage
if __name__ == "__main__":
    # Create tasks with the new interface
    task1 = create_store_value_task("user_preference", "dark_mode")
    # task2 = create_store_value_task("session_token", "xyz789", 3600)

    redis_crew.tasks = [task1]
    put_text("Starting the crew... kickoff done")
    result = redis_crew.kickoff()
    put_text("\nCrew Execution Results:")
    put_text(result)
    while True:
        put_text("Lets play with this Agent...")
        desc = input("Enter the description of the task: ")
        task = Task(
            description=desc,
            agent=redis_agent,
            expected_output="Confirmation of successful storage in Redis",
        )
        redis_crew.tasks = [task]
        agent_out = redis_crew.kickoff()
        put_text("Agent Output:")
        put_text(agent_out)
