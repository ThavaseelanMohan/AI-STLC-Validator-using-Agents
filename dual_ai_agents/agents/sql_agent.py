import datetime
import os

class SQLAgent:
    def __init__(self, model):
        self.model = model
        os.makedirs("logs", exist_ok=True)
        self.log_file = "logs/sql_agent.log"

    def log(self, message):
        """Write logs with timestamps."""
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.datetime.now()} - {message}\n")

    def generate_sql(self, mapping_text: str):
        """Generate SQL scripts from a mapping document."""
        self.log("Received mapping document for SQL generation.")
        prompt = f"""
        You are a senior data engineer. Based on this mapping document,
        generate SQL scripts that transform source data to target schema.

        Mapping Document:
        {mapping_text}

        Include CREATE TABLE (if needed) and INSERT SELECT statements.
        """
        try:
            response = self.model(prompt)
            self.log("Successfully generated SQL scripts.")
            return response
        except Exception as e:
            self.log(f"Error: {e}")
            return f"Error generating SQL scripts: {e}"
