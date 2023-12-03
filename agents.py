from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.agents.agent import AgentExecutor
from classes import DynamoDBChatMessageHistoryNew
from retrievers import *
from tools import get_tool
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
# from dotenv import load_dotenv
from tools import *
from langchain.agents import AgentType, Tool, initialize_agent

def _init_test_agent(session_id, streaming=False):
    llm_chat = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k-0613", streaming=streaming)
    tools = [
        get_general_task(),
        get_schedule_task(),
        get_time_management_tool(),
    ]
    # tool for taking task as (text, date, start time, end time)
    # tool for the user entering the steps of the task (task_name, steps)
    # tool for the user suffering from a problem
    sys_message = SystemMessage(
        content="You are an AI agent responsible for taking tasks from the user in a todo app, and answering questions related to time management and procrastination problems.\n"
                "The user will interact with you in those ways:\n"
                "1)If a user will send a task, you should ask the user for (start_time, end_time, date) of the task if the user didn't send it use schedule_task tool.\n"
                "Make sure to always take from the user the (start_time, end_time, date) of the task. NEVER FORGET THEM!!\n\n"
                "2)If a user will send you the steps of the task use the general_task tool to save the steps of the task and its title.\n\n"
                "3)If a user will send you a question regarding time management and procrastination, answer only based on the data from the time_management_database.\n"
                "Never answer anything from outside the time_management_database.\n\n"
                "Make sure to extract all the details from the user message according to the tools you have.\n\n"
                "If the user didn't give you full information, ask the user for the missing information.\n\n"
                "Never answer any questions that is not related to the todo app, or time management and procrastination.\n\n"
                "Never answer any general questions, REMEMBER that you are only a todo app agent.\n\n"
                "Use the tools you have intelligently."
    )

    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=sys_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name="chat_history")],
    )

    reminder = "Never Answer any general questions, REMEMBER that you are only a todo app agent, and only answer questions about time management and procrastination.\n\n"
    reminder += "Be intelligent and use the tools you have intelligently.\n\n"
    reminder += "use schedule_task tool to save the text, date, start time and end time of the task.\n\n"
    reminder += "use general_task tool to save the steps of the task and its title."
    reminder += "use time_management_database to answer questions about time management and procrastination."

    memory = AgentTokenBufferMemory(max_token_limit=10500, memory_key="chat_history", llm=llm_chat,
                                    chat_memory=DynamoDBChatMessageHistoryNew(table_name="langchain-agents",
                                                                              session_id=session_id, reminder=reminder))

    agent = OpenAIFunctionsAgent(llm=llm_chat, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        return_intermediate_steps=True,
        verbose=True,
    )

    return agent_executor
# enum Agent
class Agent(str, Enum):
    JEWELRY = "jewelry"
    BIZNIS_CLINICS = "biznis-clinics"
    CRYPTO = "crypto"
    ECOM = "ecom"
    BEAUTY_CLINICS = "beauty-clinics"
    DIAMONDS = "diamonds"
    TEST = "test"
    WELCH_LAW = "welch-law"


agents_dict = {
    Agent.TEST: _init_test_agent,
}

def get_agent(name, session_id, streaming=False):
    return agents_dict[name](session_id=session_id, streaming=streaming)
