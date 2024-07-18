def find_key_recursively(data, keys):
    if isinstance(data, dict):
        for k, v in data.items():
            if k in keys:
                return v
            result = find_key_recursively(v, keys)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key_recursively(item, keys)
            if result is not None:
                return result
    return None


def check_contact_info(resume_json):
    score = 100
    weightage = {
        "name": 25,
        "email": 25,
        "phone": 25,
        "linkedin": 25
    }
    
    # Retrieve contact information
    name = find_key_recursively(resume_json, ['name'])
    email = find_key_recursively(resume_json, ['email'])
    phone = find_key_recursively(resume_json, ['phone'])
    linkedin = find_key_recursively(resume_json, ['linkedin'])
    
    # Check for each contact information field and deduct points if missing
    if not name:
        score -= weightage["name"]
    
    if not email:
        score -= weightage["email"]
    
    if not phone:
        score -= weightage["phone"]
    
    if not linkedin:
        score -= weightage["linkedin"]
    
    return score


def check_qualifications(resume_json):
    score = 100
    weightage = {
        "education": 30,
        "work_experience": 40,
        "professional_certifications": 30,
    }
    
    # Retrieve qualifications
    education = find_key_recursively(resume_json, ['education'])
    work_experience = find_key_recursively(resume_json, ['work_experience'])
    professional_certifications = find_key_recursively(resume_json, ['professional_certifications'])
    
    # Check for each qualification field and deduct points if missing
    if not education:
        score -= weightage["education"]
    
    if not work_experience:
        score -= weightage["work_experience"]
    
    if not professional_certifications:
        score -= weightage["professional_certifications"]
    
    return score


def check_education(resume_json):
    score = 100
    weightage = {
        "institutions_attended": 30,
        "degrees_earned": 40,
        "graduation_dates": 30,
    }
    
    # Define search keys
    education_keys = [
        'university', 'college', 'school', 'institute', 
        'institutions_attended', 'institution', 'academy', 'higher_education', 'academic_institution', 'learning_center'
    ]
    degree_keys = [
        'degree', 'qualification', 'credentials', 'degrees_earned', 'diploma', 'qualification', 
    ]
    graduation_keys = [
        'dates', 'graduation_dates', 'expected_completion', 'start_date', 'end_date', 'graduation_year', 'completion_dates', 'culmination_dates', 'degree_conferred'
    ]
    
    # Retrieve education details using alternate keys under 'education'
    institutions_attended = find_key_recursively(resume_json.get('education', {}), education_keys)
    degrees_earned = find_key_recursively(resume_json.get('education', {}), degree_keys)
    graduation_dates = find_key_recursively(resume_json.get('education', {}), graduation_keys)
    
    # Check for each education field and deduct points if missing
    if not institutions_attended:
        score -= weightage["institutions_attended"]
    
    if not degrees_earned:
        score -= weightage["degrees_earned"]
    
    if not graduation_dates:
        score -= weightage["graduation_dates"]
    
    return score

