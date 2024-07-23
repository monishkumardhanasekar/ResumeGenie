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