import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_session import Session
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
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

def create_chat_model():
    global chat, parameters

    vertexai.init(project="eepow-project", location="us-central1")
    chat_model = ChatModel.from_pretrained("chat-bison")
    parameters = {
        "candidate_count": 1,
        "max_output_tokens": 512,
        "temperature": 0.1,
        "top_p": 0.8,
        "top_k": 40
    }
    chat = chat_model.start_chat(
        context="""Bạn là một chatbot hỗ trợ sinh viên Việt Nam học môn Lập trình hướng đối tượng. Bạn có thể giải thích các khái niệm và hướng dẫn làm bài tập Lập trình hướng đối tượng cho sinh viên. Khi giải thích các khái niệm, bạn hãy minh họa bằng code ngôn ngữ C++. Khi đưa ra code, bạn hãy giải thích tổng quan về code.""",
        examples=examples
    )

def recreate_chat_model():
    # print("Recreating chat model...")
    create_chat_model()

# Create the chat model initially
create_chat_model()

# Schedule the job every 10 minutes
# scheduler = BackgroundScheduler()
# scheduler.add_job(recreate_chat_model, 'interval', minutes=1)
# scheduler.start()

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
CORS(app, supports_credentials=True)

@app.route('/refresh', methods=['POST'])
def refresh():
    recreate_chat_model()
    return jsonify({"status": "success", "message": "Chat model recreated."})

@app.route('/predict', methods= ['POST'])
def predict():
  if request.get_json():
      x=json.dumps(request.get_json())
      x=json.loads(x)
  else:
      x={}
  data=x["text"]  # text
  response = chat.send_message(data, )
  response = jsonify(response.text)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

if __name__ == '__main__':
  app.run(port=8080, host='0.0.0.0', debug=True)
  # print(chat.send_message("Lập trình hướng đối tượng là gì vậy?", **parameters).text)

