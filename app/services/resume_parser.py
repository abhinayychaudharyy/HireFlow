import os
import fitz
import docx

SUPPORTED_FORMATS = [".pdf", ".docx"]

TECH_KEYWORDS = [
    "python", "java", "c++", "sql", "mongodb", "mysql",
    "fastapi", "django", "flask", "react", "node",
    "machine learning", "deep learning", "nlp",
    "docker", "aws", "git", "api", "rest"
]


def parse_pdf(file_path):
    text = ""
    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()
    return clean_text(text)


def parse_docx(file_path):
    text = ""
    doc = docx.Document(file_path)

    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"

    return clean_text(text)


def clean_text(text):
    lines = text.split("\n")
    return "\n".join([l.strip() for l in lines if l.strip()])


def extract_skills(text):
    text = text.lower()
    return [skill for skill in TECH_KEYWORDS if skill in text]


def extract_projects(text):
    lines = text.split("\n")
    projects = []
    capture = False

    for line in lines:
        if "project" in line.lower():
            capture = True
        elif "education" in line.lower():
            capture = False

        if capture and len(line) > 10:
            projects.append(line)

    return projects


def extract_project_technologies(projects):
    result = {}

    for proj in projects:
        result[proj] = [
            tech for tech in TECH_KEYWORDS if tech in proj.lower()
        ]

    return result


def parse_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in SUPPORTED_FORMATS:
        raise ValueError("Only PDF/DOCX allowed")

    if ext == ".pdf":
        text = parse_pdf(file_path)
    else:
        text = parse_docx(file_path)

    return {
        "raw_text": text,
        "skills": extract_skills(text),
        "projects": extract_projects(text),
        "project_technologies": extract_project_technologies(
            extract_projects(text)
        )
    }