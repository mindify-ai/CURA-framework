# main.py
from cura.agent import Agent
from dotenv import load_dotenv

load_dotenv()

code_generation_agent = Agent(
    name="Code Generation Agent",
    description="An agent that generates code based on user input.",
    tools=[],
    model="gpt-4o-mini",
    provider="openai"
)

print(code_generation_agent)

# Example of generating code
user_prompt = "Create a Python script that prints 'Hello, world!'"
generated_code = code_generation_agent.run(user_prompt)
print("\nGenerated Code:\n")
print(generated_code)
