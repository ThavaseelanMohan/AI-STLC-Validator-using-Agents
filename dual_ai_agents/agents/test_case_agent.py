import datetime
import os

class TestCaseAgent:
    def __init__(self, model):
        self.model = model
        os.makedirs("logs", exist_ok=True)
        self.log_file = "logs/test_agent.log"

    def log(self, message):
        """Write logs with timestamps."""
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.datetime.now()} - {message}\n")

    def generate_test_cases(self, requirements_text: str):
        """Generate structured test cases from a requirements document."""
        self.log("Received requirements document for test case generation.")
        prompt = f"""
        You are a QA test engineer. Read the following software requirements
        and produce structured test cases in this format:

        TestCaseID | Title | Steps | Expected Result

        Requirements:
        {requirements_text}
        """
        try:
            response = self.model(prompt)
            self.log("Successfully generated test cases.")
            return response
        except Exception as e:
            self.log(f"Error: {e}")
            return f"Error generating test cases: {e}"
