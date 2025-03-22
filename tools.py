from langchain.tools import Tool

skill_dict: dict[str, None] = {}
education_cert_dict: dict[str, dict[str, str]] = {}
work_dict: dict[str, dict[str, str]] = {}
project_dict: dict[str, dict[str, str]] = {}
hobbies_dict: dict[str, None] = {}


def get_skill_data() -> dict[str, None]:
    """Retrieve skill-related data.

    Returns:
        dict[str, None] = {}: A dict containing the applicant's skills
    """
    return skill_dict


def get_education_and_certification_data() -> dict[str, dict[str, str]]:
    """Retrieve education-related data.

    Returns:
        dict[str, dict[str, str]]: A nested dictionary with education/award
        and all the associated data such as grading and establishment.
    """
    return education_cert_dict


def get_work_data() -> dict[str, dict[str, str]]:
    """Retrieve work experience data.

    Returns:
        dict[str, dict[str, str]]: A dictionary where each key is a job title, 
        and the value is another dictionary containing details such as company 
        name, duration, and responsibilities.
    """
    return work_dict


def get_project_data() -> dict[str, dict[str, str]]:
    """Retrieve project-related data.

    Returns:
        dict[str, dict[str, str]]: A dictionary where each key is a project 
        name, and the value is another dictionary containing details such as
        description, technologies used, and outcomes.
    """
    return project_dict


def get_hobbies_data() -> dict[str, None]:
    """Retrieve hobbies and personal interests data.

    Returns:
        dict[str, None] = {}: A dict of the applicant's hobbies.
    """
    return hobbies_dict


access_skills = Tool(
    name="access_skills",
    func=get_skill_data,
    description="Get information on the applicant's skills.",
)

access_educationCertifications = Tool(
    name="access_educationCertifications",
    func=get_education_and_certification_data,
    description="""Get information on the applicant's education background and
    any certifications they have""",
)

access_workExp = Tool(
    name="access_workExp",
    func=get_work_data,
    description="Get information on the applicant's work history.",
)

access_project = Tool(
    name="access_project",
    func=get_project_data,
    description="Get information on the applicant's projects.",
)

access_hobbies = Tool(
    name="access_hobbies",
    func=get_hobbies_data,
    description="""Get information on the applicant's personal hobbies and
    interests.""",
)

