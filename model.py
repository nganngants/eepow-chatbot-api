import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from collections import Counter

chat = None
parameters = None

def load_data(filename):
  df = pd.read_csv(filename)
  examples = []
  for i in range(len(df)):
    if (len(df['answer'][i].split()) > 50):
      continue
    examples.append(InputOutputTextPair(
        input_text=df['question'][i], 
        output_text=df['answer'][i]
      )
    )
  return examples

examples = load_data('oop_qas.csv')
assert len(examples) > 0
#init vertex ai
vertexai.init(project="eepow-project", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison")
parameters = {
    "max_output_tokens": 2048,
    "temperature": 0.1,
    "top_p": 0.8,
    "top_k": 40
}
chat = chat_model.start_chat(
    context="""Bạn là một giảng viên dạy môn Lập trình hướng đối tượng ở một trường Đại học ở Việt Nam. Bạn có thể giải thích các khái niệm và hướng dẫn làm bài tập Lập trình hướng đối tượng cho sinh viên. Khi giải thích các khái niệm, bạn hãy minh họa bằng code ngôn ngữ C++. Khi đưa ra code, bạn hãy giải thích tổng quan về code.""",
    examples=examples
)

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods= ['POST'])
def predict():
  if request.get_json():
      x=json.dumps(request.get_json())
      print('ok')
      x=json.loads(x)
  else:
      x={}
  data=x["text"]  # text
  response = chat.send_message(data, **parameters)
  response = jsonify(response.text)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

if __name__ == '__main__':
  app.run(port=8080, host='0.0.0.0', debug=True)
  # print(chat.send_message("Lập trình hướng đối tượng là gì vậy?", **parameters).text)

