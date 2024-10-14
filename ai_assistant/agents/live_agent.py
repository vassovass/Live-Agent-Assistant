from ai_assistant.agents.agent_base import AgentBase
import openai

class LiveAgent(AgentBase):
    def __init__(self, config, error_handler):
        super().__init__(config, error_handler)
        self.openai_client = openai.OpenAI(api_key=config.get('openai_api_key'))

    def run(self):
        try:
            # Implement the main logic for the LiveAgent here
            self.logger.info("LiveAgent is running...")

            # Example: Get user input
            user_input = input("User: ")

            # Example: Generate a response using OpenAI
            response = self.generate_response(user_input)

            print(f"AI: {response}")

        except Exception as e:
            self.error_handler.handle_error(e, "Error in LiveAgent.run")

    def generate_response(self, user_input):
        try:
            completion = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            self.error_handler.handle_error(e, "Error in LiveAgent.generate_response")
            return "I'm sorry, I encountered an error while generating a response."
