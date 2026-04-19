from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def generate_questions(skills, projects, role):

    prompt = f"""
    You are an expert HR interviewer.

    Candidate Skills: {skills}
    Candidate Projects: {projects}
    Job Role: {role}

    Generate:
    1. 3 technical questions based on candidate's work
    2. 2 behavioral questions
    3. 2 scenario-based questions

    Make questions specific to candidate experience.
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content