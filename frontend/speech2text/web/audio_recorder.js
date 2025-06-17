//This script was created with the help of an employee from the company I collaborated with for the project workshop

let mediaRecorder;
let audioChunks = [];
let stream; 

function initRecorder() {
  console.log('Recorder initialized');
}

async function startRecording() {
  try {
    
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    audioChunks = [];
    mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = event => {
      audioChunks.push(event.data);
    };
    
    mediaRecorder.start();
    console.log('Recording started');
  } catch (error) {
    console.error('Error starting recording:', error);
  }
}

function stopRecording(callback) {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.onstop = () => {
      let blob = new Blob(audioChunks, { type: 'audio/wav' });
      let reader = new FileReader();
      reader.onload = () => {
        let arrayBuffer = reader.result;
        let byteArray = new Uint8Array(arrayBuffer);
        
        // Stop to release the microphone.
        stopAllTracks();
        
        callback(byteArray);
      };
      reader.readAsArrayBuffer(blob);
    };
    mediaRecorder.stop();
  } else {
    // If it's not recording
    stopAllTracks();
  }
}

function stopAllTracks() {
  if (stream) {
    stream.getTracks().forEach(track => {
      track.stop();
      console.log('Audio track stopped');
    });
    stream = null;
  }
}

function forceStopRecording() {
  if (mediaRecorder) {
    if (mediaRecorder.state === 'recording') {
      mediaRecorder.stop();
    }
    mediaRecorder = null;
  }
  stopAllTracks();
  audioChunks = [];
  console.log('Recording force stopped');
}

window.addEventListener('beforeunload', () => {
  forceStopRecording();
});

