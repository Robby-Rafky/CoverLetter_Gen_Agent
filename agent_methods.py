import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from tools import get_available_tools


ERROR_MESSAGES = {
    "429": "Error: Rate limit exceeded. Please wait before trying again.",
    "400": "Error: Bad request. Try again.",
    "401": "Error: Unauthorized. Check your API key.",
    "403": "Error: Forbidden. Access to the resource denied.",
    "404": "Error: Resource not found. Check the model name or endpoint.",
    "500": "Error: Internal server error. Try again later.",
    "503": "Error: Service unavailable. Please wait and retry.",
}


class CoverLetterAgent:
    def __init__(self):
        load_dotenv(dotenv_path="config/.env")

        self.system_prompt = self._load_system_prompt(
            "config/system_prompt.txt")

        self.llm = ChatOpenAI(
            model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            temperature=0.7,
            max_tokens=500,
            openai_api_base="https://api.together.xyz/v1",
            openai_api_key=os.getenv("TOGETHER_API_KEY")
        )

        self.tools = get_available_tools()

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

    def _load_system_prompt(self, path) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def generate_cover_letter(self, job_posting):
        prompt = f"{self.system_prompt}\nJob Posting: {job_posting}"

        try:
            response = self.agent.run(prompt)
            return response.strip()
        except Exception as e:
            self.parse_error(error_message=str(e))

    def parse_error(self, error_message) -> str:
        code = next((c for c in ERROR_MESSAGES if
                     f"Error code: {c}" in error_message), None)
        return ERROR_MESSAGES.get(
            code, f"Error generating cover letter: {error_message}")
