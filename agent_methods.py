import os
import json
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


with open("config/system_prompt.txt", "r", encoding="utf-8") as sys_file:
    system_prompt = sys_file.read()

with open("config/api_config.json", "r", encoding="utf-8") as api_file:
    api_config = json.load(api_file)


class CoverLetterAgent:
    """
    Agent to generate cover letters using a language model with available
    tools.
    """
    def __init__(self):
        """
        Initialize the agent, load environment variables, and set up LLM and
        tools.

        Loads the API key from environment variables and initializes the LLM
        with the specified model and parameters. Sets up available tools and
        configures the agent.
        """
        load_dotenv(dotenv_path="config/.env")

        self.llm = ChatOpenAI(
            model_name=api_config["model"],
            temperature=0.7,
            max_tokens=500,
            openai_api_base=api_config["api_base"],
            openai_api_key=os.getenv("TOGETHER_API_KEY")
        )

        self.tools = get_available_tools()

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

    def generate_cover_letter(self, job_posting):
        """
        Generate a cover letter based on the provided job posting.

        Args:
            job_posting (str): The job posting description used to generate
                               the cover letter.

        Returns:
            str: The generated cover letter, or an error message if an
                 exception occurs.
        """
        prompt = f"{system_prompt}\nJob Posting: {job_posting}"

        try:
            response = self.agent.run(prompt)
            return response.strip()
        except Exception as e:
            self.parse_error(error_message=str(e))

    def parse_error(self, error_message) -> str:
        """
        Parse error messages and return a user-friendly error description.

        Args:
            error_message (str): The raw error message returned by the model.

        Returns:
            str: A user-friendly error message or a default error message if
                 the error code is unknown.
        """
        code = next((c for c in ERROR_MESSAGES if
                     f"Error code: {c}" in error_message), "Unknown Error")
        return ERROR_MESSAGES.get(
            code, f"Error generating cover letter: {error_message}")
