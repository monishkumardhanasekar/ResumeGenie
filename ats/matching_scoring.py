# ats/matching_scoring.py

def score_resume_against_job(resume_data, job_data):
    scores = {}

    # Skill Matching
    resume_skills = set(resume_data.get('skills', {}).get('languages', []) +
                        resume_data.get('skills', {}).get('frameworks_libraries', []) +
                        resume_data.get('skills', {}).get('tools', []))
    required_skills = set(job_data.get('required_skills', []))

    skill_match_count = len(resume_skills & required_skills)
    skill_score = (skill_match_count / len(required_skills)) * 100 if required_skills else 0

    # Education Matching
    education_match = any(
        degree.lower() in str(resume_data.get('education', [{}])[0].get('degree', '')).lower()
        for degree in job_data.get('education_requirements', [])
    )
    education_score = 100 if education_match else 0

    # Experience Matching
    resume_experience_years = resume_data.get('experience_years', 0)  # Optional: calculate from work experience if needed
    required_experience_years = job_data.get('experience_required_years', 0)
    experience_score = 100 if resume_experience_years >= required_experience_years else 50

    # Title Matching
    resume_titles = [exp.get('title', '') for exp in resume_data.get('work_experience', [])]
    title_match = any(
        title.lower() in " ".join(resume_titles).lower()
        for title in job_data.get('titles', [])
    )
    title_score = 100 if title_match else 0

    # Weighted Total Score
    total_score = (0.4 * skill_score) + (0.2 * education_score) + (0.2 * experience_score) + (0.2 * title_score)

    scores['skill_score'] = skill_score
    scores['education_score'] = education_score
    scores['experience_score'] = experience_score
    scores['title_score'] = title_score
    scores['total_score'] = total_score

    return scores
