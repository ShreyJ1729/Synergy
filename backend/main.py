"""
Main web application service. Serves the static frontend as well as
API routes for transcription, language model generation and text-to-speech.
"""
import json
from pathlib import Path
import modal
import time
from common import stub
from transcriber import Whisper
from pydantic import BaseModel
from fastapi import FastAPI, Request
from gpt import call_gpt
import openai
import os
import dotenv

SYSTEM_PROMPT = """
- You speak like a charismatic human, NOT A HELPFUL AI ASSISTANT.  You respond the way humans verbally converse.
- You are direct, concise, but approachable and fun sometimes. You get straight to the point and help move the discussion forward with the user. Refrain from meaningless sentences that an assistant would say, like "I see you're trying to <X>." No human to human conversation goes like that.
- Talk like humans, the way they lead people into following their thoughts with phrases like "right?" and "so,", and similarly persuasive but concise wording.
- You are not a text based AI assistant, you are an expert at small-talk and respond in human conversation. This is NOT a text message experience, this is a verbal conversation.
- Important! You are in the middle of a live conversation with a human, and will have to start thinking of your response even if you don't have the full sentence from the human.  Deduce where their thought is going, and start constructing your response to them. Identify the persons mood, attitude, and likely direction of conversation. Specify if you think we should interject with should_we_speak based on how confident you are in the context of conversation.
Criteria for when we should speak:
- if user is going off on too many different tangents, interrupt them, because you're supposed to help them brainstorm productively
- if user strays from their original intention, keep them on topic, be blunt if they get distracted.
- if you think we have enough information about key features / entities / attributes of what the person is talking about.
- if the user is unclear about something they're talking about.
Structure your responses as such:
{"should_we_speak":"true/false", "generated": "<your response to user>"}
"""

dotenv.load_dotenv(".env")
openai.api_key = os.environ["OPENAI_API_KEY"]

stub.chat_contexts = modal.Dict.new()


def find_assistant_true_index(id):
    for i, context in enumerate(stub.chat_contexts[id]):
        if context["role"] == "assistant" and "true" in context["content"]:
            return i
    return -1


@stub.function(
    container_idle_timeout=60,
    timeout=60,
)
@modal.web_endpoint(method="POST")
async def determine_response(request: Request):
    id = request.query_params["id"]
    print(stub.chat_contexts)

    response = (
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=stub.chat_contexts[id],
            temperature=0.75,
            max_tokens=250,
            top_p=1,
            frequency_penalty=0.22,
            presence_penalty=0.21,
        )
        .choices[0]
        .message.content
    )

    summary = None
    if "true" in response:
        last_assitant_idx = find_assistant_true_index(id)
        # Summarize the last few chunks
        if last_assitant_idx != -1:
            return -1
        # Get all the content from the last assistant index to the end
        # Format it where you concatenate the role: \n content \n\n
        # Then send it to GPT-4

        content = ""
        for i in range(last_assitant_idx, len(stub.chat_contexts[id])):
            content += (
                stub.chat_contexts[id][i]["role"]
                + ":\n"
                + stub.chat_contexts[id][i]["content"]
                + "\n\n"
            )

        summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that summarizes the conversation the conversation between a user trying to brainstorm and an AI trying to keep the user on task. The user just finished a thought and you need to summarize it. Use the given conversation to do so.",
                },
                {"role": "user", "content": content},
            ],
        )

    stub.chat_contexts[id].append({"role": "assistant", "content": response})

    return response, summary["choices"][0]["message"]["content"]


@stub.function(
    cpu=8,
    gpu="A10G",
    timeout=10,
)
@modal.web_endpoint(method="POST")
async def transcribe(request: Request):
    from fastapi.responses import Response, StreamingResponse
    from fastapi.staticfiles import StaticFiles

    transcriber = Whisper()
    id = request.query_params["id"]
    bytes = await request.body()

    result = transcriber.transcribe_segment.remote(bytes)
    if id not in stub.chat_contexts:
        stub.chat_contexts[id] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    stub.chat_contexts[id].append({"role": "user", "content": result["text"]})

    return result["text"]
