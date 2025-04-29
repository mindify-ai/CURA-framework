import os
import requests

class Agent:
    def __init__(self, name: str, description: str, tools: list, models: str, api_key: str = None):
        self.name = name
        self.description = description
        self.tools = tools
        self.models = models
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key is required. Set it via argument or OPENROUTER_API_KEY env var.")

    def __repr__(self):
        return (f"<Agent(name={self.name!r}, "
                f"description={self.description!r}, "
                f"tools={self.tools!r}, "
                f"models={self.models!r})>")
        
    def __str__(self):
        return (f"Agent: {self.name}\n"
                f"Description: {self.description}\n"
                f"Tools: {', '.join(self.tools) if self.tools else 'None'}\n"
                f"Models: {self.models}\n")
        
    def __call__(self, user_input: str) -> str:
        """
        Calls the OpenRouter API to generate code based on user input.
        """
        return self.run(user_input)
    
    def get_tools(self) -> list:
        """
        Returns the list of tools available to the agent.
        """
        return self.tools

    def run(self, user_input: str) -> str:
        """
        Actually calls OpenRouter to generate code based on user input.
        """
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.models,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that generates high-quality Python code based on user input."},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"OpenRouter API call failed: {response.status_code} {response.text}")

        data = response.json()
        return data['choices'][0]['message']['content'].strip()
