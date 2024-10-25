from flask import Flask, request, jsonify
import os
import requests

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"
api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

def transcribe_audio(file_path):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
    }
    files = {
        'file': (file_path, open(file_path, "rb")),
        'model': (None, "whisper-1")
    }
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        transcription = response.json()
        return transcription['text']
    else:
        return None

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Get the file path from the request
    file_path = request.json.get("file_path")
    transcription = transcribe_audio(file_path)
    return jsonify({"transcription": transcription})

if __name__ == "_main_":
    app.run(debug=True)
