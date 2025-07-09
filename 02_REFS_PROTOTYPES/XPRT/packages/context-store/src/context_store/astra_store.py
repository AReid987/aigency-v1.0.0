# packages/context-store/src/astra_store.py
from astrapy.db import AstraDB
from datetime import datetime
import os

class DevelopmentHistory:
    def __init__(self):
        self.db = AstraDB(
            api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
            token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
            namespace="aider_context"
        )
        self.collection = self.db.collection("development_steps")
    
    # Use temporary credentials
    def get_astra_client():
        return AstraDB(
            api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
            token=os.getenv("ASTRA_DB_TEMP_TOKEN"),  # Rotated token
            namespace="aider_context"
        )
    
    def log_operation(self, operation: dict):
        """Store LLM development actions"""
        document = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation['type'],
            "files": operation['files'],
            "prompt_hash": hash(operation['prompt']),
            "code_snapshot": self._get_code_snapshot(operation['files'])
        }
        return self.collection.insert_one(document)