import re
import sys
import threading
import slack
from pinecone import Pinecone, ServerlessSpec
import os
from time import sleep, time
from pathlib import Path
from flask import Flask
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
from pinecone_plugins.assistant.models.chat import Message

env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)

app = Flask(__name__)
import pdb
pdb.set_trace()
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events',app)
client = slack.WebClient(token=os.environ['BOT_SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']
# client.chat_postMessage(channel='#python_bot', text="Hello World!")
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

assistant = pc.assistant.Assistant(
    assistant_name=os.environ.get("ASSISTANT_NAME"), 
)

processed_messages = {}
MESSAGE_EXPIRY_TIME = 10 
#TODO - Create Task to delete the processed_messages for every 12 hour

def query_pinecone(query_text):
    chat_context = [Message(content=query_text)]
    response = assistant.chat_completions(messages=chat_context)
    print(processed_messages)
    return response

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    subtype = event.get('subtype')

    if BOT_ID != user_id and (subtype is None or subtype != 'bot_message'):
        message_key = (channel_id, text)
        
        current_time = time()
        if message_key not in processed_messages or (current_time - processed_messages[message_key]) > MESSAGE_EXPIRY_TIME:
            processed_messages[message_key] = current_time
            response_text = query_pinecone(text)
            if response_text:
                response = response_text['choices'][0]['message']['content'].split('References:')[0].replace('**', '*')
                response = re.sub(r'\[\d+(, pp\.\s*\d+(-\d+)?(, \d+(-\d+)?)*?)?\]', '', response)
                client.chat_postMessage(channel=channel_id, text=response)

if __name__ == '__main__':
    app.run(debug=True)
