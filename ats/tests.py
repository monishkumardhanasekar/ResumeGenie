from django.test import TestCase

# Create your tests here.
# # Initialize Gramformer
# gf = Gramformer(models='grammar')  # Ensure you have the model files downloaded

# def check_grammar(text):
#     try:
#         errors = gf.correct(text)
#         # Return detailed errors if they exist
#         if errors is None:
#             return [], False
#         return errors, len(errors) > 0
#     except Exception as e:
#         print(f"Error checking grammar: {e}")
#         return [], False

# # Initialize PySpellChecker
# spell = SpellChecker()

# def check_spelling(text):
#     words = re.findall(r'\b\w+\b', text.lower())
#     misspelled = spell.unknown(words)
#     return list(misspelled)

# def check_spelling_and_grammar(resume_text):
#     score = 100
#     weightage = {
#         "grammar": 30,
#         "spelling": 30,
#     }

#     # Check grammar errors
#     grammar_errors, has_grammar_errors = check_grammar(resume_text)
#     if has_grammar_errors:
#         score -= weightage["grammar"]

#     # Check spelling errors
#     spelling_errors = check_spelling(resume_text)
#     if spelling_errors:
#         score -= weightage["spelling"]

#     return score, grammar_errors, spelling_errors








# from textblob import TextBlob

# def check_spelling_errors(text):
#     blob = TextBlob(text)
#     corrected_text = blob.correct()
    
#     # Split both texts into words for comparison
#     original_words = text.split()
#     corrected_words = corrected_text.split()
    
#     # Find spelling mistakes by comparing original and corrected texts
#     spelling_mistakes = [word for word, corrected in zip(original_words, corrected_words) if word != corrected]
#     return spelling_mistakes

#     # # Calculate the spelling errors score
#     # total_words = len(original_words)
#     # mistakes_count = len(spelling_mistakes)
#     # score = max(0, 100 - (mistakes_count / total_words * 100))  # Example scoring formula

#     # return score

# from spellchecker import SpellChecker

# def check_spelling_errors(resume_text):
#     """
#     Check for spelling errors in the extracted resume text.
#     """
#     spell = SpellChecker()
    
#     # Split the text into words
#     words = resume_text.split()
    
#     # Find misspelled words
#     misspelled = spell.unknown(words)
#     return list(misspelled)
    
#     # Calculate the number of errors
#     num_errors = len(misspelled)
    
#     # Score starts at 100
#     score = 100
    
#     # Deduct points for each spelling error (example: 2 points per error)
#     deduction_per_error = 2
#     score -= num_errors * deduction_per_error
    
#     # Ensure score is not negative
#     if score < 0:
#         score = 0
    
#     return score