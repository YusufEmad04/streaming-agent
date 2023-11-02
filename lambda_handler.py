from agents import get_agent, Agent
import json


def lambda_handler(event, context):
    # if event["requestContext"]["http"]["method"] == "POST":
    body = json.loads(event["body"])
    question = body["question"]
    session_id = body["session_id"]

    agent = get_agent(Agent.TEST, session_id)

    try:
        response = agent(question)["output"]
    except Exception as e:
        # return an error with status code suitable for the error
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"answer": response}),
    }
