# agent/llm_agent.py
import os
from openai import OpenAI

class LLMAgent:
    def __init__(self):
        # Fetch API Key from environment variables safely
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        # Fallback to hardcoded string ONLY if environment variable isn't set
        if not api_key or api_key == "your_actual_api_key_here":
            # REMEMBER: Change this to your real DeepSeek API key (e.g., "sk-...")
            api_key = "your_actual_api_key_here" 

        # The base URL must be exactly this for the OpenAI SDK
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    def chat(self, prompt_string: str) -> dict:
        """
        Hits the real DeepSeek API and returns a structured response 
        matching what your FastAPI core expects.
        """
        try:
            # We use 'deepseek-v4-pro' which is the flagship API model.
            response = self.client.chat.completions.create(
                model="deepseek-v4-pro",  
                messages=[
                    {"role": "system", "content": "You are the SantoArt core data assistant. Answer the user's questions clearly."},
                    {"role": "user", "content": str(prompt_string)}
                ],
                temperature=0.7,
                stream=False
            )
            
            # Extract content safely
            answer_content = response.choices[0].message.content
            
            # Structure the output so your existing app code doesn't break
            return {
                "answer": answer_content,
                "sql_queries": [],
                "charts": [],
                "diagrams": [],
                "tool_calls_made": ["DEEPSEEK_API"]
            }
        except Exception as e:
            # This print statement will output the EXACT error to your console/terminal 
            # so you can see if it's an Authentication (API Key) or Network error.
            print(f"--- [DEEPSEEK CRITICAL ERROR] ---: {e}")
            raise RuntimeError(f"DeepSeek API call failed: {e}")