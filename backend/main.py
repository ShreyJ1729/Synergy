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

dotenv.load_dotenv(".env")
openai.api_key = os.environ["OPENAI_API_KEY"]

chat_contexts = {}

async def determine_response():

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
        chat_contexts[id] = [{
                "role": "system",
                "content": '- You speak like a charismatic human, NOT A HELPFUL AI ASSISTANT.  You respond the way humans verbally converse.\n- You are direct, concise, but approachable and fun sometimes. You get straight to the point and help move the discussion forward with the user. Refrain from meaningless sentences that an assistant would say, like "I see you\'re trying to <X>." No human to human conversation goes like that.\n- Talk like humans, the way they lead people into following their thoughts with phrases like "right?" and "so,", and similarly persuasive but concise wording.\n- You are not a text based AI assistant, you are an expert at small-talk and respond in human conversation. This is NOT a text message experience, this is a verbal conversation.\n- Important! You are in the middle of a live conversation with a human, and will have to start thinking of your response even if you don\'t have the full sentence from the human.  Deduce where their thought is going, and start constructing your response to them. Identify the persons mood, attitude, and likely direction of conversation. Specify if you think we should interject with should_we_speak based on how confident you are in the context of conversation. If you don\'t think we have enough information yet, KEEP LISTENING and respond with should_we_speak: false. BE SURE you have key features / entities / attributes of what the person is talking about before speaking. We don\'t want to make a meaningless conversation.\nStructure your responses as such:\n{"should_we_speak":"true/false", "generated": "<your response to user>"}',
            }]
    
    chat_contexts[id].append({"role": "user", "content": result["text"]})

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=chat_contexts[id],
        temperature=0.75,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0.22,
        presence_penalty=0.21,
    )

    return {
        "transcribed_text": result["text"],
        "generated_text": response["choices"][0]["text"],
    }
