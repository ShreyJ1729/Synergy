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
 If you don't think we have enough information yet, KEEP LISTENING and respond with should_we_speak: false. We don't want to make a meaningless conversation.
Structure your responses as such:
{"should_we_speak":"true/false", "generated": "<your response to user>"}
"""

dotenv.load_dotenv(".env")
openai.api_key = os.environ["OPENAI_API_KEY"]

chat_contexts = {}


@stub.function(
    container_idle_timeout=60,
    timeout=60,
)
@modal.web_endpoint(method="POST")
async def determine_response(request: Request):
    id = request.query_params["id"]
    response = (
        openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=chat_contexts[id],
            temperature=0.75,
            max_tokens=250,
            top_p=1,
            frequency_penalty=0.22,
            presence_penalty=0.21,
        )
        .choices[0]
        .message.content
    )

    return response


@stub.function(
    cpu=12,
    memory=4096,
    gpu="A10G",
    container_idle_timeout=60,
    timeout=60,
)
@modal.web_endpoint(method="POST")
async def transcribe(request: Request):
    from fastapi.responses import Response, StreamingResponse
    from fastapi.staticfiles import StaticFiles

    transcriber = Whisper()
    bytes = await request.body()
    id = request.query_params["id"]

    result = transcriber.transcribe_segment.call(bytes)
    if id not in chat_contexts:
        chat_contexts[id] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    chat_contexts[id].append({"role": "user", "content": result["text"]})

    return result["text"]
