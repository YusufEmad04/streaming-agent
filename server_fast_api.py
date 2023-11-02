from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from agents import get_agent, Agent
from callbacks_handlers import *


app = FastAPI()

# stream endpoint that receives json (question, session_id) and returns a streamed response
@app.post("/stream")
async def stream_response(data: dict):
    question = data["question"]
    session_id = data["session_id"]

    agent = get_agent(Agent.TEST, session_id, streaming=True)

    return StreamingResponse(run_agent(agent, question), media_type='text/plain')

# run the server
# uvicorn server_fast_api:app --reload