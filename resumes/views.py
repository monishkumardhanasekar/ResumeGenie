import json
from django.shortcuts import render, redirect
from .forms import ResumeUploadForm
from .models import Resume
from .openai_utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt, get_resume_details_from_ai
from dotenv import load_dotenv
from pymongo import MongoClient  # Import the MongoClient from PyMongo
import os

# Load environment variables from .env file
load_dotenv()


def upload_resume(request):
    extracted_text = None
    ai_json = None
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
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

            return render(request, 'upload_resume.html', {'form': form, 'extracted_text': extracted_text, 'ai_json': ai_json})
    else:
        form = ResumeUploadForm()
    return render(request, 'upload_resume.html', {'form': form, 'extracted_text': extracted_text, 'ai_json': ai_json})

def success(request):
    return render(request, 'success.html')
