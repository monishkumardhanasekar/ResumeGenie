import json
from django.shortcuts import render, redirect
from .forms import ResumeUploadForm
from .models import Resume
from .openai_utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, get_resume_details_from_ai
from ats.scoring import check_contact_info, check_qualifications, check_education, check_work_experience, check_project_experience, check_quantification_metrics, check_spelling_grammar
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import re

# Load environment variables from .env file
load_dotenv()

def clean_extracted_text(text):
    # Remove leading and trailing whitespace
    text = text.strip()
    
    # Normalize line breaks
    text = re.sub(r'\r\n', '\n', text)  # Replace Windows line breaks with Unix line breaks
    text = re.sub(r'\r', '\n', text)    # Replace old Mac line breaks with Unix line breaks
    
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove tabs
    text = re.sub(r'\t+', ' ', text)
    
    
    # Fix common OCR errors (optional, add more as needed)
    text = re.sub(r'\s*-\s*\n\s*', '', text)  # Join hyphenated line breaks
    text = re.sub(r'\s*_\s*\n\s*', '', text)  # Join underscored line breaks

    
    # Normalize punctuation spacing
    text = re.sub(r'\s*([,!?;])\s*', r'\1 ', text)
    
    # Normalize capitalization (optional, this is very context dependent)
    text = re.sub(r'(?<=[\.\!\?]\s)(\w+)', lambda m: m.group(1).capitalize(), text)

    #  # Remove sequences of three or more consecutive dashes, underscores, or other non-numeric symbols
    # text = re.sub(r'[-_]{3,}', '', text)  # Remove three or more consecutive dashes or underscores
    
   # Remove sequences of three or more consecutive non-alphanumeric symbols, excluding URL patterns
    text = re.sub(r'(https?:\/\/[^\s]+)|[^a-zA-Z0-9\s]{3,}', lambda m: m.group(1) if m.group(1) else '', text)
    
    return text



def upload_resume(request):
    extracted_text = None
    ai_json = None
    ats_score_contact = None
    ats_score_qualification = None
    ats_score_education = None
    ats_score_work_experience = None
    ats_score_project_experience = None
    ats_score_quantification_metrics = None
    ats_score_spelling_grammar_errors = None

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()

            # Get file and its extension
            file = resume.file
            file_ext = file.name.split('.')[-1].lower()

            # Extract text based on file type
            if file_ext == 'pdf':
                extracted_text = extract_text_from_pdf(file)
            elif file_ext == 'docx':
                extracted_text = extract_text_from_docx(file)
            elif file_ext == 'txt':
                extracted_text = extract_text_from_txt(file)

            # Clean extracted text
            if extracted_text:
                extracted_text = clean_extracted_text(extracted_text)

            # Get AI response
            if extracted_text:
                ai_response = get_resume_details_from_ai(extracted_text)
                
                # Extract JSON from AI response
                try:
                    start_index = ai_response.find('{')
                    end_index = ai_response.rfind('}') + 1
                    json_str = ai_response[start_index:end_index]
                    ai_json = json.loads(json_str)  # Convert JSON string to Python dictionary
                    
                    # Save the JSON to MongoDB
                    mongo_uri = os.getenv('MONGODB_URI')
                    db_name = os.getenv('MONGODB_DB_NAME')
                    collection_name = os.getenv('MONGODB_COLLECTION_NAME')
                    client = MongoClient(mongo_uri)
                    db = client[db_name]
                    resumes_collection = db[collection_name]
                    resumes_collection.update_one(
                        {'_id': resume.id},  # Match the resume document by its ID
                        {'$set': {'ai_json': ai_json}},  # Add the JSON data to the 'ai_json' field
                        upsert=True
                    )
                    
                    # Calculate ATS score
                    ats_score_contact = check_contact_info(ai_json)
                    ats_score_qualification = check_qualifications(ai_json)
                    ats_score_education = check_education(ai_json)
                    ats_score_work_experience = check_work_experience(ai_json)
                    ats_score_project_experience = check_project_experience(ai_json)  # Calculate project experience score
                    ats_score_quantification_metrics = check_quantification_metrics(ai_json)
                    ats_score_spelling_grammar_errors = check_spelling_grammar(extracted_text)  # Calculate spelling errors score

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

            return render(request, 'upload_resume.html', {'form': form, 'extracted_text': extracted_text, 'ai_json': ai_json, 'ats_score_contact': ats_score_contact, 'ats_score_qualification': ats_score_qualification, 'ats_score_education': ats_score_education, 'ats_score_work_experience': ats_score_work_experience, 'ats_score_project_experience': ats_score_project_experience, 'ats_score_quantification_metrics': ats_score_quantification_metrics, 'ats_score_spelling_grammar_errors': ats_score_spelling_grammar_errors})
    else:
        form = ResumeUploadForm()
    return render(request, 'upload_resume.html', {'form': form, 'extracted_text': extracted_text, 'ai_json': ai_json, 'ats_score_contact': ats_score_contact})

def success(request):
    return render(request, 'success.html')