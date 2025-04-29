import os
import requests
from openai import OpenAI

class Agent:
    def __init__(
        self,
        name: str,
        description: str,
        tools: list,
        model: str,
        provider: str = None,
        openai_api_key: str = None,
        openrouter_api_key: str = None,
    ):
        """
        Agent initializer supports both OpenAI and OpenRouter providers.
        """
        self.name = name
        self.description = description
        self.tools = tools
        self.model = model

        # Determine provider
        self.provider = provider or os.getenv("AGENT_PROVIDER", "openai")
        if self.provider not in ("openai", "openrouter"):
            raise ValueError("Provider must be 'openai' or 'openrouter'.")

        # Load API keys
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.openrouter_api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")

        # Initialize clients based on provider
        if self.provider == "openai":
            if not self.openai_api_key:
                raise ValueError(
                    "OpenAI API key is required for provider 'openai'."
                    " Set it via argument or OPENAI_API_KEY env var."
                )
            # Initialize OpenAI client (v1.0.0+)
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            if not self.openrouter_api_key:
                raise ValueError(
                    "OpenRouter API key is required for provider 'openrouter'."
                    " Set it via argument or OPENROUTER_API_KEY env var."
                )

    def __repr__(self):
        return (
            f"<Agent(name={self.name!r}, "
            f"description={self.description!r}, "
            f"tools={self.tools!r}, "
            f"model={self.model!r}, "
            f"provider={self.provider!r})>"
        )

    def __str__(self):
        return (
            f"Agent: {self.name}\n"
            f"Description: {self.description}\n"
            f"Tools: {', '.join(self.tools) if self.tools else 'None'}\n"
            f"Model: {self.model}\n"
            f"Provider: {self.provider}\n"
        )

    def __call__(self, user_input: str) -> str:
        return self.run(user_input)

    def get_tools(self) -> list:
        return self.tools

    def run(self, user_input: str) -> str:
        if self.provider == "openai":
            return self._run_openai(user_input)
        return self._run_openrouter(user_input)

    def _run_openai(self, user_input: str) -> str:
        """
        Uses the OpenAI Python SDK v1.0.0 interface.
        """
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": (
                    "You are a helpful assistant that generates high-quality Python code "
                    "based on user input.")},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()

    def _run_openrouter(self, user_input: str) -> str:
        """
        Calls the OpenRouter REST API to generate a completion.
        """
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": (
                    "You are a helpful assistant that generates high-quality Python code "
                    "based on user input.")},
                {"role": "user", "content": user_input}
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(
                f"OpenRouter API call failed: {response.status_code} {response.text}"
            )
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

# Example usage:
# agent = Agent(
#     name="CodeGen",
#     description="Generates Python code",
#     tools=["print", "os"],
#     model="gpt-4o-mini",
#     provider="openai"
# )
# print(agent("Write a function to reverse a string in Python."))
