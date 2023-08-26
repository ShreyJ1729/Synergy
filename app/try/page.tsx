'use client';
import React, { useState, useEffect, useRef, useCallback } from 'react';
import RecorderNode from './recorder-node';

let mediaRecorder: MediaRecorder | null = null;
let recordedChunks = [];
let mediaStream;
let audioCtx;
let analyzer;
let interval;
let recorderNode;


function stopRecording() {
  mediaRecorder?.stop();
  if(interval) clearInterval(interval)
  interval = null
  audioCtx.close()
  audioCtx = null

  mediaRecorder.onstop = () => {
    let blob = new Blob(recordedChunks, {
      'type' : 'audio/ogg; codecs=opus'
    });
    recordedChunks = [];
    mediaStream.getTracks().forEach(track => track.stop());
    mediaStream = null;
    //let audioURL = window.URL.createObjectURL(blob);
  };
}

async function fetchTranscript(buffer) {
  const blob = new Blob([buffer], { type: "audio/float32" });
  return
  const response = await fetch("/transcribe", {
    method: "POST",
    body: blob,
    headers: { "Content-Type": "audio/float32" },
  });

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
  async function onMount() {
    onSegmentRecv(new Float32Array())
    let constraints = { audio: true };

    mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
    audioCtx = new AudioContext();
    const source = audioCtx.createMediaStreamSource(mediaStream)
    await audioCtx.audioWorklet.addModule('processor.js');
    recorderNodeRef.current = new RecorderNode(
      audioCtx, 
      onSegmentRecv,
      () => {
        setIsSilence(true)
        setIsTalking(false)
      },
      () => {
        setIsSilence(false)
        setIsTalking(true)
      }
    )
    source.connect(recorderNodeRef.current)
    recorderNodeRef.current.connect(audioCtx.destination)
  }
  
  useEffect(() => {
    onMount();
  }, []);

  useEffect(() => {
    if(isRecording) {
      recorderNodeRef.current?.start()
    } else {
      recorderNodeRef.current?.stop()
    }
  }, [isRecording])

  const onSegmentRecv = useCallback(
    async (buffer) => {
      console.log(buffer)
      const data = await fetchTranscript(buffer);
      if (buffer.length) {
        // TODO
      }
    },
    [history]
  );

  return (
    <main className='h-screen w-full bg-gray-200'>
      <button onClick={() => setIsRecording(!isRecording)}>
        <svg width={16} className={`fill-none inline ${isRecording ? "!stroke-red-500" : ""}`} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
      </button>
      {isTalking && <div>talking</div>}
      {isSilence && <div>silence</div>}
    </main>
  );

};

export default Dashboard;
