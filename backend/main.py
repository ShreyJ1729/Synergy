"""
Main web application service. Serves the static frontend as well as
API routes for transcription, language model generation and text-to-speech.
"""

import json
from pathlib import Path
import modal

from common import stub
from transcriber import Whisper


@stub.function(
    container_idle_timeout=300,
    timeout=600,
)
@modal.web_endpoint(method="POST")
async def transcribe():
    from fastapi import FastAPI, Request
    from fastapi.responses import Response, StreamingResponse
    from fastapi.staticfiles import StaticFiles

    transcriber = Whisper()
    bytes = await request.body()
    result = transcriber.transcribe_segment.call(bytes)
    return result["text"]
