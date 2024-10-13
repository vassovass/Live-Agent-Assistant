
import logging
from models.model_base import ModelBase
import openai

class GPTInterface(ModelBase):
    def __init__(self, config, error_handler):
        super().__init__(config, error_handler)
        self.api_key = self.config.get('openai_api_key')
        openai.api_key = self.api_key

    def generate_plan(self, text):
        try:
            self.logger.debug("Generating plan using GPT model...")
            response = openai.Completion.create(
                engine="gpt-4",
                prompt=f"Create a detailed plan based on the following input:

{text}",
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            plan = response.choices[0].text.strip()
            self.logger.debug(f"Generated plan: {plan}")
            return plan
        except Exception as e:
            self.logger.exception("Error generating plan with GPT: %s", e)
            self.error_handler.handle(e)
            return None

    def generate_response(self, prompt):
        try:
            self.logger.debug("Generating response using GPT model...")
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            generated_text = response.choices[0].text.strip()
            self.logger.debug(f"Generated response: {generated_text}")
            return generated_text
        except Exception as e:
            self.logger.exception("Error generating response with GPT: %s", e)
            self.error_handler.handle(e)
            return None
