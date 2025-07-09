# packages/aider-pilot/src/aider_core.py
from langchain_core.prompts import ChatPromptTemplate
from langchain import ChatOpenAI
from code_graph import CodeContext

class AiderCore:
    # TODO: api base & api key gemini or openrouter api
    def __init__(self, repo_root: str):
        self.context = CodeContext(repo_root)
        self.graph = self.context.build_code_graph()
        self.llm = ChatOpenAI(
            model="gemini-flash-2.0-exp",
            api_base="",
            api_key=""
        )
        
    async def process_message(self, message: str) -> str:
        # Augment prompt with code context
        augmented_prompt = self._augment_prompt(message)
        
        # Generate response
        response = await self.llm.ainvoke(augmented_prompt)
        
        # Apply code changes
        self._apply_code_edits(response.code_edits)
        
        return response.text
    
    def _augment_prompt(self, prompt: str) -> str:
        return f"""
        [CODE CONTEXT]
        {self.graph.summary()}
        
        [USER PROMPT]
        {prompt}
        
        [INSTRUCTIONS]
        1. Analyze existing code structure
        2. Propose changes considering all Turborepo projects
        3. Output diffs in unified format
        """