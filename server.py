from flask import Flask, Response, request
import time

# add cors support
from flask_cors import CORS
from agents import get_agent, Agent
from callbacks_handlers import *

app = Flask(__name__)
CORS(app)

def generate():
    for i in range(10):
        time.sleep(0.2)  # Simulating some delay
        print(i)
        yield str(i)

@app.route('/stream', methods=['GET', 'POST'])
def stream_response():

    # json is question and session_id
    # receive json

    data = request.get_json()
    question = data["question"]
    session_id = data["session_id"]

    agent = get_agent(Agent.TEST, session_id, streaming=True)

    return Response(run_agent(agent, question), content_type='text/plain')

app.run(host='0.0.0.0', port=5000, debug=True)
