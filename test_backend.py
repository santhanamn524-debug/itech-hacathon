
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

try:
    from backend.agent.llm_agent import process_user_query
    print("[INIT] Loaded process_user_query successfully!")
    
    # Mocking your client configuration context
    class MockClient:
        def __init__(self):
            self.chat = self
            self.completions = self
        def create(self, **kwargs):
            class MockMessage:
                content = "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines."
                tool_calls = None
            class MockChoice:
                message = MockMessage()
            class MockResponse:
                choices = [MockChoice()]
            return MockResponse()

    test_input = "what is ai"
    print("\n--- RUNNING BACKEND FUNCTION ---")
    result = process_user_query(test_input, MockClient())
    print("\n[SUCCESS] Response:")
    print(result)
    
except Exception as e:
    import traceback
    traceback.print_exc()

