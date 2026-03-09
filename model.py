from langgraph.graph import START, END, StateGraph
from typing import List, Annotated, TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph.message import BaseMessage
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv
from pinecone import Pinecone
import requests
# We send a POST request with the 'text' key expected by your FastAPI Query model
                

load_dotenv()
PINECONE_KEY = os.getenv('PINECONE_KEY')
API_URL = os.getenv('API_URL')


cilent = Pinecone(api_key=PINECONE_KEY)

index_name = 'medicine-info-embed'
index = cilent.Index(host='dynamic-chatbot-2t52grx.svc.aped-4627-b74a.pinecone.io')


class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


def ChatNode(state: ChatState):
  if not any(isinstance(m, SystemMessage) for m in state['messages']):
    mess = SystemMessage(content=
                  """
                  You are an AI assistant that answers only questions related to the company’s policies and official business information using the provided database text.
                  If the user’s question cannot be answered from the given data, reply:
                  “Sorry, I can’t answer that.”
                  """)
    state['messages'].insert(0, mess)


  message = state['messages'][-1]

  pine_output = index.search(namespace='company',query={"top_k": 1,"inputs": {"text": message.content}})['result']['hits'][0]['fields']['text']

  if isinstance(message, HumanMessage):
    prompt = f"""
              Company Data: {pine_output}\n\n
              User Question: {message.content}
              """
  else:
    prompt = message.content
  print(prompt)

  payload = {"text": prompt}
  response = requests.post(API_URL, json=payload, timeout=60)
  if response.status_code == 200:
    answer = response.json().get("response", "No response key found.")

  if ':' in answer:
    result = answer.split(':')[-1].strip()
  else:
    result = answer

  return {'messages': [AIMessage(content = result)]}


graph = StateGraph(ChatState)
graph.add_node('chatnode',ChatNode)

graph.add_edge(START, 'chatnode')
graph.add_edge('chatnode', END)

workflow = graph.compile()