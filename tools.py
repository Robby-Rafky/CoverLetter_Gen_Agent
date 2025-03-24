import json
from langchain.tools import Tool


def get_work_history() -> dict[str, dict[str, str | None]] | str:
    return read_applicant_data("Work History")


def get_education_awards() -> dict[str, dict[str, str | None]] | str:
    return read_applicant_data("Education & Awards")


def get_projects() -> dict[str, dict[str, str | None]] | str:
    return read_applicant_data("Projects")


def get_skills() -> dict[str, None] | str:
    return read_applicant_data("Skills")


def get_hobbies() -> dict[str, None] | str:
    return read_applicant_data("Hobbies")


def read_applicant_data(file_name):
    with open(f"applicant data/{file_name}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data.pop(next(iter(data)))
    return data if data else "No information available"


def get_available_tools():
    with open("config/tool_descriptions.json", "r", encoding="utf-8") as f:
        desc = json.load(f)

    tools = [
        Tool(
            name="get_skills",
            func=lambda _: get_skills(),
            description=desc["get_skills"]
        ),
        Tool(
            name="get_work_history",
            func=lambda _: get_work_history(),
            description=desc["get_work_history"]
        ),
        Tool(
            name="get_education_awards",
            func=lambda _: get_education_awards(),
            description=desc["get_education_awards"]
        ),
        Tool(
            name="get_projects",
            func=lambda _: get_projects(),
            description=desc["get_projects"]
        ),
        Tool(
            name="get_hobbies",
            func=lambda _: get_hobbies(),
            description=desc["get_hobbies"]
        )
    ]
    return tools