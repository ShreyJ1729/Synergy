'use client';
import React, { useState } from 'react';

let mediaRecorder: MediaRecorder | null = null;
let recordedChunks = [];
let mediaStream;
let audioCtx;
let analyzer;
let interval;
async function startRecording() {
  let constraints = { audio: true };
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
    audioCtx = new AudioContext();
    analyzer = audioCtx.createAnalyser();
    audioCtx.createMediaStreamSource(mediaStream).connect(analyzer);
    let arr = new Uint8Array(100)
    interval = setInterval(() => {
      analyzer.getByteFrequencyData(arr)
      console.log(arr)
    }, 250)

    mediaRecorder = new MediaRecorder(mediaStream);
    mediaRecorder.start();

    mediaRecorder.ondataavailable = (e) => {
      recordedChunks.push(e.data);
      console.log('chunk')
    };
  } catch (err) {
    console.error('The following error occurred: ' + err);
  }
}

function stopRecording() {
  mediaRecorder?.stop();
  if(interval) clearInterval(interval)
  interval = null
  analyzer.disconnect()
  audioCtx.close()
  analyzer = null
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

const Dashboard = () => {
  const [isRecording, setIsRecording] = useState(false);
  function onMic() {
    if(isRecording) {
      stopRecording();
      setIsRecording(false);
    } else {
      startRecording();
      setIsRecording(true);
    }
  }

  return (
    <button onClick={onMic}>
      <svg width={16} className={`fill-none inline ${isRecording ? "!stroke-red-500" : ""}`} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-mic"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
    </button>
  );
  
};

export default Dashboard;
