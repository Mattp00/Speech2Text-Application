from flask import Flask, render_template,  request, jsonify #,url,for
from flask_cors import CORS
import os
from transformers import WhisperProcessor
from transformers import WhisperForConditionalGeneration

from werkzeug.utils import secure_filename
import torch
import torchaudio
from pydub import AudioSegment

WHISPER_MODEL = "Sandiago21/whisper-large-v2-italian"
LANGUAGE = "it"

# Determine device
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Initialize processor and model
processor = WhisperProcessor.from_pretrained(WHISPER_MODEL, language=LANGUAGE, task="transcribe")
model = WhisperForConditionalGeneration.from_pretrained(WHISPER_MODEL)

# Move model to device
model = model.to(device)

model.generation_config.language = "it"
model.generation_config.task = "transcribe"
model.config.forced_decoder_ids = None
model.generation_config.forced_decoder_ids = None

#The hugging face pipelien can be used to transcribe the audio using a single component
#whisper = pipeline('automatic-speech-recognition', model = 'Sandiago21/whisper-large-v2-italian')

# Function to convert audio to WAV at 16 kHz
def convert_to_wav_16k(file_path):
    """
    Converts an audio file to WAV format with 16 kHz sampling rate and single channel.
    
    Args:
        file_path (str): The path of the audio file to convert
    
    Returns:
        str: The path of the converted WAV file
    """
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    wav_path = "converted_audio.wav"
    audio.export(wav_path, format="wav")
    return wav_path

def perform_transcription(file_path):
    """
    Performs transcription of an audio file using the Whisper model.
    
    Args:
        file_path (str): The path of the audio file to transcribe
    
    Returns:
        str: The transcription of the audio file
    
    Raises:
        FileNotFoundError: If the specified file does not exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Convert file to WAV format with single channel and 16KHz sampling rate
    file_path = convert_to_wav_16k(file_path)

    # Extract audio file and sampling rate
    waveform, sample_rate = torchaudio.load(file_path)
    waveform = waveform[0] 
    
    # Feature Extractor + Tokenizer
    inputs = processor(waveform, sampling_rate=sample_rate, return_tensors="pt")

    # Move inputs to the same device as the model
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Generate transcription
    with torch.no_grad():
        predicted_ids = model.generate(inputs["input_features"], max_length=448)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    #print(transcription[0])
    return transcription[0]


app = Flask(__name__)
CORS(app)

AUDIO_FOLDER = 'fileAudio'

@app.route('/')
def index():
    """
    Main route that returns the index HTML page.
    
    Returns:
        str: The rendered HTML template
    """
    return render_template('index.html')

@app.route('/upload_audio', methods=['POST'])
def upload():
    """
    Endpoint to upload and transcribe audio files.
    
    Returns:
        tuple: A tuple containing the JSON response and HTTP status code
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file in the folder
    filename = secure_filename(file.filename)
    file_path = os.path.join(AUDIO_FOLDER, filename)
    file.save(file_path)

    # Perform transcription of the audio file
    transcription = perform_transcription(file_path)
    print(transcription)

    # Return the transcription in the message body
    return jsonify({'message': 'File uploaded successfully',
                    'output': transcription }), 200

# This method was created to test the REST operations with the client
@app.route('/api', methods = ['GET'])
def return_ascii():
    """
    API endpoint that converts a character to its ASCII value.
    
    Returns:
        Response: JSON response containing the ASCII value of the character
    """
    d = {}
    input_char = str(request.args['query'])
    answer = str(ord(input_char))
    d['output'] = answer
    return jsonify(d)

""" TODO: Sockets are probably more efficient for this type of operations.
@sockets.route('/receiveAudio')
def audio_socket(ws):
    audio_file_path = os.path.join(AUDIO_FOLDER, 'streamed_audio.wav')
    wf = wave.open(audio_file_path, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(44100)

    while not ws.closed:
        message = ws.receive()
        if message:
            wf.writeframes(message)
    wf.close()
    """

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        Response: JSON response indicating service status
    """
    return jsonify({
        'status': 'healthy',
        'model': WHISPER_MODEL,
        'device': device,
        'language': LANGUAGE
    })

if __name__ == "__main__":
    print(f"Starting Flask app with Whisper model: {WHISPER_MODEL}")
    print(f"Language: {LANGUAGE}")
    print(f"Device: {device}")
    app.run(debug=True, host='127.0.0.1', port=5000)

