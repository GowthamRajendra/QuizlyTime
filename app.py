from flask import Flask, jsonify, request
import requests
from html import unescape

app = Flask(__name__)

URL = "https://opentdb.com/api.php?"

@app.route('/questions', methods=['GET'])
def get_ques():
    amount = request.json.get('amount')
    type = request.json.get('type')
    difficulty = request.json.get('difficulty')
    category = request.json.get('category')

    response = requests.get(URL + f'amount={amount}&category={category}&difficulty={difficulty}&type={type}').json()
    for ques in response["results"]:
        ques["question"] = unescape(ques["question"])
        ques["correct_answer"] = unescape(ques["correct_answer"])
        for i in range(len(ques["incorrect_answers"])):
            ques["incorrect_answers"][i] = unescape(ques["incorrect_answers"][i])
    
    # print(response['results'])
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
