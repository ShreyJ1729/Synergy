const VOICE_ID = '21m00Tcm4TlvDq8ikWAM'

export async function talkBack(text) {
  const stream = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}/stream`,
  { 
    method: 'POST', 
    headers: { 
      'Content-Type': 'application/json',
      'xi-api-key': process.env.NEXT_PUBLIC_ELEVEN_API_KEY,
      

    }, 
    responseType: 'arraybuffer',
    body: JSON.stringify({
      text,
      model_id: "eleven_monolingual_v1",
      voice_settings: {
        stability: 0,
        similarity_boost: 0,
        style: 0,
        use_speaker_boost: true
      }
    }) 
  })

  const context = new AudioContext()
  
  context.decodeAudioData(await stream.arrayBuffer(), (buffer) => {
    const source = context.createBufferSource()
    source.buffer = buffer
    source.connect(context.destination)
    source.start(0)
  })
}

if(typeof window !== 'undefined') {
  window.talkBack = talkBack
}