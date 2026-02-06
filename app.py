import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"



def push(message: str):
    if not PUSHOVER_USER or not PUSHOVER_TOKEN:
        return
    payload = {
        "user": PUSHOVER_USER,
        "token": PUSHOVER_TOKEN,
        "message": message
    }
    requests.post(PUSHOVER_URL, data=payload)



def record_user_details(email: str, name: str = "Not provided", notes: str = "Not provided"):
    push(f"New contact → Name: {name}, Email: {email}, Notes: {notes}")
    return {"status": "recorded"}


def record_unknown_question(question: str):
    push(f"Unanswered question: {question}")
    return {"status": "recorded"}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Record user contact details",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "name": {"type": "string"},
                    "notes": {"type": "string"},
                },
                "required": ["email"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "record_unknown_question",
            "description": "Record a question the assistant could not answer",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                },
                "required": ["question"]
            },
        },
    },
]


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        tool_fn = globals().get(name)
        if tool_fn:
            result = tool_fn(**args)
        else:
            result = {}

        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    return results



reader = PdfReader("me/linkedin.pdf")
linkedin_text = ""
for page in reader.pages:
    if page.extract_text():
        linkedin_text += page.extract_text()

with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

NAME = "Nanda Gopal"

SYSTEM_PROMPT = f"""
You are acting as {NAME}.
You are answering questions on {NAME}'s website related to career, background, skills, and experience.
Use the following information:
LinkedIn Profile:
{linkedin_text}
Summary:
{summary}
Be professional, concise, and helpful.
"""



def chat(message, history):
    history_msgs = [{"role": h["role"], "content": h["content"]} for h in history]

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + history_msgs
        + [{"role": "user", "content": message}]
    )

    while True:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=TOOLS,
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            tool_results = handle_tool_calls(msg.tool_calls)
            messages.extend(tool_results)
        else:
            return msg.content



with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Career Conversation")
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### About Me")
            gr.Markdown(summary)
            gr.Markdown("### Capabilities")
            gr.Markdown(
                "- Answer questions about my career\n"
                "- Record contact details\n"
                "- Log unanswered questions"
            )
        with gr.Column(scale=2):
            gr.ChatInterface(chat, type="messages")

demo.launch()
