from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
import asyncio

class CallbackHandler(StreamingStdOutCallbackHandler):

    def on_llm_new_token(self, token: str, **kwargs: any) -> None:
        print(token, end="")
        # should yield to a generator for returing a chunked http response


    def on_llm_end(self, response, **kwargs) -> None:
        print(response, end="")

async def run_call(agent, query, handler):
    agent.agent.llm.callbacks = [handler]
    await agent.acall({"input": query})

async def run_agent(agent, query):
    handler = AsyncIteratorCallbackHandler()
    task = asyncio.create_task(run_call(agent, query, handler))
    async for token in handler.aiter():
        if token is not None and token != "":
            yield token

    await task
