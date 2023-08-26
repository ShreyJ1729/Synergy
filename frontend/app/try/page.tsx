"use client";
import React, { useState, useEffect, useRef, useCallback } from "react";
import RecorderNode from "./recorder-node";
import Navbar from "../navbar";
import { talkBack } from "./eleven";

let mediaRecorder: any = null;
let recordedChunks: any[] = [];
let mediaStream: any = null;
let audioCtx: any = null;
let analyzer;
let interval: any = null;
let recorderNode;

function stopRecording() {
  mediaRecorder?.stop();
  if (interval) clearInterval(interval);
  interval = null;
  audioCtx.close();
  audioCtx = null;

  mediaRecorder.onstop = () => {
    let blob = new Blob(recordedChunks, {
      type: "audio/ogg; codecs=opus",
    });
    recordedChunks = [];
    mediaStream.getTracks().forEach((track: any) => track.stop());
    mediaStream = null;
    //let audioURL = window.URL.createObjectURL(blob);
  };
}

async function fetchTranscript(buffer: any) {
  const blob = new Blob([buffer], { type: "audio/float32" });
  const response = await fetch(
    `https://shreyj1729--synergy-transcribe.modal.run/${location.search}`,
    {
      method: "POST",
      body: blob,
      headers: { "Content-Type": "audio/float32" },
    }
  );

  if (!response.ok) {
    console.error("Error occurred during transcription: " + response.status);
  }

  return await response.json();
}
const Dashboard = () => {
  const [isRecording, setIsRecording] = useState(false);
  const recorderNodeRef = useRef<RecorderNode>(null);
  const [isTalking, setIsTalking] = useState(false);
  const [isSilence, setIsSilence] = useState(false);
  const [summary, setSummary] = useState("");
  const chatBoxRef = useRef<HTMLDivElement>(null);
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

  const [transcript, setTranscript] = useState([]);

  const appendTranscript = useCallback(
    (data) => {
      setTranscript((transcript) => [...transcript, data?.trim()]);
      setTimeout(() => chatBoxRef.current.scrollTo(0, 99999), 100);
    },
    [transcript, chatBoxRef]
  );

  const onSegmentRecv = useCallback(async (buffer) => {
    const data = await fetchTranscript(buffer);
    const json = data[0];
    const sum = data[1];
    setSummary(sum);
    console.log(sum);
    if (sum.length) {
      appendTranscript(sum);
    }
  }, []);
  return (
    <>
      <Navbar />
      <main className="w-full h-screen p-4">
        <div className="absolute -translate-y-1/4 -translate-x-20 h-[400px] w-[1000px] rounded-full bg-gradient-to-tr from-[#00306088] via-[#1b998b88] to-[#ade25d11] blur-[250px] content-[''] z-[-1]"></div>
        <div className="flex flex-col items-center gap-2">
          <div
            ref={chatBoxRef}
            className="h-24 overflow-y-auto"
            style={{
              WebkitMaskImage:
                transcript.length >= 4 &&
                "-webkit-gradient(linear, left top, left bottom, from(rgba(0,0,0,0)), to(rgba(0,0,0,1)))",
            }}
          >
            {transcript.map((t, i) => (
              <p key={i}>{t}</p>
            ))}
          </div>

          <svg
            className={`my-auto fill-none inline ${
              isTalking ? "!stroke-red-500" : ""
            }`}
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
          <div>{{ summary }}</div>
        </div>
      </main>
    </>
  );
};

export default Dashboard;
