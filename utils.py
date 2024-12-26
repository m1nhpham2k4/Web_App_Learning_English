from flask import jsonify
from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import re
import torch
import time
import pandas as pd
from eng_to_ipa import ipa_list
from setting import embedding_speech

def preprocess_text(text: str) -> str:    
    if pd.isnull(text):
        return " "
    text = re.sub(r"['\",\.\?:\-!]", "", text)
    text = text.strip()
    text = " ".join(text.split())
    text = text.lower()
    return text

synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts", device='cpu')
# embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embedding_speech).unsqueeze(0)
def make_response(data={}, status=200):
    """
    - Make a resionable response with header
    - status default is 200 mean ok
    """
    res = jsonify(data)
    res.headers.add("Content-Type", "application/json")
    res.headers.add("Accept", "application/json")
    return res
def text_to_speech(text):
    name = text.replace(' ', '_')
    # time.sleep(2)
    speech = synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})
    # tts = gTTS(text=text, slow=False)
    # tts.save(f"./templates/audio/{name}.mp3")
    
    sf.write(f"./templates/audio/{name}.mp3", speech["audio"], samplerate=speech["sampling_rate"])

    return f"./audio/{name}.mp3"
    
def addipa(text):
    word = ipa_list(text)
    ipa = []
    for w in word:
        ipa.append(w[0])
    return ' '.join(ipa)
