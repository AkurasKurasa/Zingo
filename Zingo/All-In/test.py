import json
import paths

try:
    with open(paths.QUESTIONS_JSON_PATH, 'r') as file:
        data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    data = []  

new_question = {
    "question_type": "Short Answer",
    "question": "What is the capital of the Philippines?",
    "answer": "Manila"
}

data.append(new_question)

with open(paths.QUESTIONS_JSON_PATH, 'w') as file:
    json.dump(data, file, indent=4)