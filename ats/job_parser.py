# ats/job_parser.py

import re

# ➡️ Predefine basic lists (you can expand these later)
SKILLS = [
    'Python', 'Java', 'AWS', 'Django', 'React', 'Node.js', 'Machine Learning', 
    'Deep Learning', 'Docker', 'Kubernetes', 'PostgreSQL', 'MongoDB'
]

DEGREES = [
    'Bachelor', 'Bachelors', 'Master', 'Masters', 'PhD', 'Doctorate', 'MBA'
]

TITLES = [
    'Software Developer', 'Software Engineer', 'Data Scientist', 'Backend Developer', 'Frontend Developer'
]

def parse_job_description(text):
    parsed = {
        'required_skills': [],
        'education_requirements': [],
        'titles': [],
        'experience_required_years': 0,
    }

    text_lower = text.lower()

    # Match skills
    for skill in SKILLS:
        if skill.lower() in text_lower:
            parsed['required_skills'].append(skill)

    # Match education
    for degree in DEGREES:
        if degree.lower() in text_lower:
            parsed['education_requirements'].append(degree)

    # Match titles
    for title in TITLES:
        if title.lower() in text_lower:
            parsed['titles'].append(title)

    # Extract years of experience
    experience_match = re.search(r'(\d+)\+?\s*(years|yrs)', text_lower)
    if experience_match:
        parsed['experience_required_years'] = int(experience_match.group(1))

    return parsed
