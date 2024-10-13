from abc import abstractmethod
import anthropic
from openai import OpenAI


available_models = {
    "claude-3-5-sonnet-20240620": "Anthropic",
    "claude-3-sonnet-20240229": "Anthropic",
    "claude-3-haiku-20240307": "Anthropic",
    "claude-3-opus-20240229": "Anthropic",
    "gpt-3.5-turbo": "OpenAI",
    "gpt-4-turbo": "OpenAI",
    "gpt-4o-mini": "OpenAI",
}


system_message = """
You are a expert who helps the user building up their knowledge.
The user is asked to explain a concept from the selected category, and you are here to provide feedback.
Please make sure they understood the concept, and its importance with regard to the selected category.
Illustrate the bridges and interaction with other related concepts.
The ability to go beyond the definition and understand the interaction between multiple concepts is fundamental.
"""


def get_user_prompt(category: str, concept: str, user_message: str) -> str:
    return f"""
    In the category "{category}", I have selected the concepts: "{concept}". Here are my understanding:
    {user_message}
    """


class LLMInterface:
    def __init__(self):
        self.client = None

    @abstractmethod
    def create_client(self, api_key: str) -> any:
        ...

    def set_api_key(self, api_key: str) -> str:
        try:
            self.client = self.create_client(api_key=api_key)
            return "API key set successfully!"
        except Exception as e:
            return f"Error setting API key: {str(e)}"

    @abstractmethod
    def api_call(self, model:str, user_message: str) -> str:
        ...

    def query(self, model:str, category: str, concept: str, user_message: str) -> str:
        if not self.client:
            return "Please set your API key first."

        user_prompt = get_user_prompt(category, concept, user_message)

        try:
            return self.api_call(model, user_prompt)
        except Exception as e:
            return f"Error querying LLM API: {str(e)}"


class AnthropicInterface(LLMInterface):
    def create_client(self, api_key: str) -> any:
        return anthropic.Client(api_key=api_key)

    def api_call(self, model:str, user_message: str) -> str:
        response = self.client.messages.create(
            model=model,
            max_tokens=1000,
            system=system_message,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_message,
                        }
                    ],
                }
            ],
        )
        return response.content[0].text


anthropic_interface = AnthropicInterface()


class OpenaiInterface(LLMInterface):
    def create_client(self, api_key: str) -> any:
        return OpenAI(api_key=api_key)

    def api_call(self, model:str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content


openai_interface = OpenaiInterface()


def llm_interface_call(
    model: str, api_key: str, category: str, concept: str, user_message: str
) -> str:
    if model in available_models:
        if available_models[model] == "Anthropic":
            interface = anthropic_interface
        elif available_models[model] == "OpenAI":
            interface = openai_interface
        else:
            return "Model not available."
    else:
        return "Model not available."

    if api_key:
        set_key_result = interface.set_api_key(api_key)
        if "Error" in set_key_result:
            return set_key_result

    return interface.query(model, category, concept, user_message)
