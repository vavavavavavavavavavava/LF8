"""
This is a Test
"""
import requests

url = "https://opentdb.com/api.php?amount=10&category=15&type=multiple"

def getQuestions():
    '''Pulls Questions from the Open Trivia DB'''
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        questions = data.get('results', [])

        for question in questions:
            print(f"Question: {question['question']}")
            print(f"Options: {question['incorrect_answers'] + [question['correct_answer']]}")
            print(f"Correct Answer: {question['correct_answer']}")
            print('-' * 50)
    else:
        print("Error fetching questions") 

getQuestions()
