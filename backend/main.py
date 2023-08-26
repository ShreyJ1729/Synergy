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
    for i, context in enumerate(chat_contexts[id]):
        if context['role'] == 'assistant' and 'true' in context['content']:
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

    stub.chat_contexts[id].append({"role": "assistant", "content": response})
    summary = None
    if 'true' in response:
        last_assitant_idx = find_assistant_true_index(id)
        # Summarize the last few chunks
        if last_assitant_idx != -1:
            return -1
        # Get all the content from the last assistant index to the end
        # Format it where you concatenate the role: \n content \n\n
        # Then send it to GPT-4

        content = ""
        for i in range(last_assitant_idx, len(stub.chat_contexts[id])):
            content += stub.chat_contexts[id][i]['role'] + ":\n" + stub.chat_contexts[id][i]['content'] + "\n\n"

        summary = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0,
            messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that summarizes the conversation the conversation between a user trying to brainstorm and an AI trying to keep the user on task. The user just finished a thought and you need to summarize it. Use the given conversation to do so."
            },
            {
                "role": "user",
                "content": content
            }
        ]
        )

    stub.chat_contexts[id].append({"role": "assistant", "content": response})

    return response, summary


@stub.function(
    cpu=8,
    gpu="A10G",
    timeout=10,
)
@modal.web_endpoint(method="POST")
async def transcribe(request: Request):
    print(f"streaming transcription of audio to client...")
    audio_data = await request.body()
    return StreamingResponse(stream_whisper(audio_data), media_type="text/event-stream")


# ---
# runtimes: ["runc", "gvisor"]
# ---
import asyncio
import io
import logging
import pathlib
import re
import tempfile
import time
from typing import Iterator

import modal
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse


def load_audio(data: bytes, sr: int = 16000):
    import ffmpeg
    import numpy as np

    try:
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        fp.write(data)
        fp.close()
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(fp.name, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(
                cmd=["ffmpeg", "-nostdin"],
                capture_stdout=True,
                capture_stderr=True,
            )
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def split_silences(
    path: str, min_segment_length: float = 30.0, min_silence_length: float = 0.8
) -> Iterator[tuple[float, float]]:
    """
    Split audio file into contiguous chunks using the ffmpeg `silencedetect` filter.
    Yields tuples (start, end) of each chunk in seconds.

    Parameters
    ----------
    path: str
        path to the audio file on disk.
    min_segment_length : float
        The minimum acceptable length for an audio segment in seconds. Lower values
        allow for more splitting and increased parallelizing, but decrease transcription
        accuracy. Whisper models expect to transcribe in 30 second segments, so this is the
        default minimum.
    min_silence_length : float
        Minimum silence to detect and split on, in seconds. Lower values are more likely to split
        audio in middle of phrases and degrade transcription accuracy.
    """
    import ffmpeg

    silence_end_re = re.compile(
        r" silence_end: (?P<end>[0-9]+(\.?[0-9]*)) \| silence_duration: (?P<dur>[0-9]+(\.?[0-9]*))"
    )

    metadata = ffmpeg.probe(path)
    duration = float(metadata["format"]["duration"])

    reader = (
        ffmpeg.input(str(path))
        .filter("silencedetect", n="-10dB", d=min_silence_length)
        .output("pipe:", format="null")
        .run_async(pipe_stderr=True)
    )

    cur_start = 0.0
    num_segments = 0

    while True:
        line = reader.stderr.readline().decode("utf-8")
        if not line:
            break
        match = silence_end_re.search(line)
        if match:
            silence_end, silence_dur = match.group("end"), match.group("dur")
            split_at = float(silence_end) - (float(silence_dur) / 2)

            if (split_at - cur_start) < min_segment_length:
                continue

            yield cur_start, split_at
            cur_start = split_at
            num_segments += 1

    # silencedetect can place the silence end *after* the end of the full audio segment.
    # Such segments definitions are negative length and invalid.
    if duration > cur_start and (duration - cur_start) > min_segment_length:
        yield cur_start, duration
        num_segments += 1
    print(f"Split {path} into {num_segments} segments")


@stub.function(cpu=2)
def transcribe_segment(
    audio_data: bytes,
    model: str,
):
    import torch
    import whisper

    t0 = time.time()
    use_gpu = torch.cuda.is_available()
    device = "cuda" if use_gpu else "cpu"
    model = whisper.load_model(model, device=device)
    np_array = load_audio(audio_data)
    result = model.transcribe(np_array, language="en", fp16=use_gpu)  # type: ignore

    return result


async def stream_whisper(audio_data: bytes):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(audio_data)
        f.flush()
        segment_gen = split_silences(f.name)

    for result in transcribe_segment.starmap(
        segment_gen, kwargs=dict(audio_data=audio_data, model="base.en")
    ):
        # Must cooperatively yeild here otherwise `StreamingResponse` will not iteratively return stream parts.
        # see: https://github.com/python/asyncio/issues/284
        await asyncio.sleep(0.5)
        yield result["text"]
