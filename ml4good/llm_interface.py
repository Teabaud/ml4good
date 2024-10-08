import anthropic


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


class AnthropicInterface:
    def __init__(self):
        self.client = None

    def set_api_key(self, api_key: str) -> str:
        try:
            self.client = anthropic.Client(api_key=api_key)
            return "API key set successfully!"
        except Exception as e:
            return f"Error setting API key: {str(e)}"

    def query_anthropic(self, category: str, concept: str, user_message: str) -> str:
        if not self.client:
            return "Please set your API key first."

        user_prompt = get_user_prompt(category, concept, user_message)

        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                system=system_message,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_prompt,
                            }
                        ],
                    }
                ],
            )
            return response.content[0].text
        except Exception as e:
            return f"Error querying Anthropic API: {str(e)}"


interface = AnthropicInterface()


def llm_interface_call(
    api_key: str, category: str, concept: str, user_message: str
) -> str:
    if api_key:
        set_key_result = interface.set_api_key(api_key)
        if "Error" in set_key_result:
            return set_key_result

    return interface.query_anthropic(category, concept, user_message)
