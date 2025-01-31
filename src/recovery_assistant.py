from typing import List, Dict
import openai

class RecoveryAssistant:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.conversation_history = []

    async def chat(self, user_input: str) -> str:
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            response = await openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a compassionate addiction recovery assistant..."},
                    *self.conversation_history
                ]
            )
            
            assistant_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            return f"Error: {str(e)}"

    async def initial_assessment(self, user_data: dict) -> dict:
        """Perform initial addiction assessment"""
        prompt = self._create_assessment_prompt(user_data)
        response = await self._get_completion(prompt)
        return self._parse_assessment(response)
        
    async def create_recovery_plan(self, assessment: dict) -> dict:
        """Generate personalized recovery plan"""
        prompt = self._create_plan_prompt(assessment)
        response = await self._get_completion(prompt)
        return self._parse_plan(response)