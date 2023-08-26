"use client";
import React, { useState, useEffect, useRef, useCallback } from "react";
import RecorderNode from "./recorder-node";
import Navbar from "../navbar";
import { talkBack } from './eleven'
//import { useWhisper } from '@chengsokdara/use-whisper'
//import { SSE } from 'sse.js'

let mediaRecorder: MediaRecorder | null = null;
let recordedChunks = [];
let mediaStream;
let audioCtx;
let analyzer;
let interval;
let recorderNode;

async function getGptResponse() {
  const resp = await fetch(`https://shreyj1729--synergy-determine-response.modal.run/${location.search}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  })
  if (!resp.ok) {
    console.error("Error occurred during GPT response: " + resp.status);
  }
  const [gptResponse, summary] = await resp.json();
  if(typeof gptResponse === "string") {
    try {
      return [JSON.parse(gptResponse), summary]
    } catch (e) {
      return [gptResponse, summary]
    }
  }
  return [gptResponse, summary]
}

async function fetchTranscript(buffer) {
    const blob = new Blob([buffer], { type: "audio/float32" });
    const resp = await fetch(`https://shreyj1729--synergy-transcribe.modal.run/${location.search}`,
      {
        method: "POST",
        body: blob,
        headers: { "Content-Type": "audio/float32" },
      }
    );
    if (!resp.ok) {
      console.error("Error occurred during transcription: " + resp.status);
    }
    const text = await resp.json();
    return text
    // eventStream.addEventListener('error', (e) => {
    //   console.error(e)
    //   reject(e)
    // });
    // eventStream.addEventListener('message', (e) => {
    //   console.log(e)
    //   if(e.data === '[DONE]') {
    //     resolve()
    //   }
    // });
    // eventStream.stream()
}

const Dashboard = () => {
  const [isRecording, setIsRecording] = useState(false);
  const recorderNodeRef = useRef<RecorderNode>(null);
  const [isTalking, setIsTalking] = useState(false);
  const [isSilence, setIsSilence] = useState(false);
  const [transcript, setTranscript] = useState([]);
  const [gptResponse, setGptResponse] = useState(null);
  const [summary, setSummary] = useState(null);
  const [gptQueued, setGptQueued] = useState(false);
  const [isGptRunning, setIsGptRunning] = useState(false);

  const chatBoxRef = useRef<HTMLDivElement>(null);
  
  const runGpt = useCallback(async () => {
    if (isGptRunning) {
      return;
    }
    setIsGptRunning(true);
    const resp = await getGptResponse();
    console.log(resp)

    const [gptResponse, summary] = resp;
    if (gptResponse) {
      setGptResponse(gptResponse);
    }
    setSummary(summary);
    if((gptResponse?.should_we_speak === true || gptResponse?.should_we_speak === 'true') && gptResponse?.generated?.length) {
      await talkBack(gptResponse.generated)
    }
    setIsGptRunning(false);
  }, [gptQueued, isGptRunning]);

  async function onMount() {
    onSegmentRecv(new Float32Array());
    let constraints = { audio: true };

    mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
    audioCtx = new AudioContext();
    const source = audioCtx.createMediaStreamSource(mediaStream);
    await audioCtx.audioWorklet.addModule("processor.js");
    recorderNodeRef.current = new RecorderNode(
      audioCtx,
      onSegmentRecv,
      () => {
        setIsSilence(true);
        setIsTalking(false);
      },
      () => {
        setIsSilence(false);
        setIsTalking(true);
      }
    );
    source.connect(recorderNodeRef.current);
    recorderNodeRef.current.connect(audioCtx.destination);
  }

  useEffect(() => {
    onMount();
    recorderNodeRef.current?.start();
  }, []);

  useEffect(() => {
    if (isRecording) {
      recorderNodeRef.current?.start();
    } else {
      recorderNodeRef.current?.stop();
    }
  }, [isRecording]);

  const appendTranscript = useCallback(
    (data) => {
      setTranscript((transcript) => ([...transcript, data?.trim()]));
      setTimeout(() => chatBoxRef.current.scrollTo(0, 99999), 100);
    },
    [transcript, chatBoxRef]
  );
  
  const onSegmentRecv = useCallback(
    async (buffer) => { 
      const data = await fetchTranscript(buffer)
      appendTranscript(data);
      setGptQueued(true);
      runGpt();
    }, []
  );
  // const { transcript: tr } = useWhisper({
  //   apiKey: process.env.NEXT_PUBLIC_OPENAI_API_TOKEN, // YOUR_OPEN_AI_TOKEN
  //   streaming: true,
  //   timeSlice: 1_000, // 1 second
  //   whisperConfig: {
  //     language: 'en',
  //   },
  //   autoStart: true
  // })
  //const transcript = [tr?.text]
  return (
    <>
    <Navbar />
    <main className="p-4 h-screen w-full text-xl font-semibold">
    <div className="absolute -translate-y-1/4 -translate-x-20 h-[400px] w-[1000px] rounded-full bg-gradient-to-tr from-[#00306088] via-[#1b998b88] to-[#ade25d11] blur-[250px] content-[''] z-[-1]"></div>
      <div className='flex gap-2 flex-col items-center'>
        <div ref={chatBoxRef} className="overflow-y-auto h-48" style={{
          WebkitMaskImage: transcript?.length >= 4 && '-webkit-gradient(linear, left top, left bottom, from(rgba(0,0,0,0)), to(rgba(0,0,0,1)))'
        }}>{transcript?.map((t, i) => (<p key={i}>{t}</p>))}</div>

        <svg
          className={`my-auto fill-none inline ${isTalking ? "!stroke-red-500" : ""}`}
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
        {gptResponse && <div className="text-center">{gptResponse.generated}</div>}
        {summary && <div className="text-center">{summary}</div>}
      </div>
    </main>
    </>
  );
};

export default Dashboard;
