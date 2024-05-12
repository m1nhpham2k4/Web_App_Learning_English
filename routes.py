from flask import request
from models import *
from app import app, db
from flask import request
import pandas as pd
import time 
from flask import jsonify
from flask_cors import CORS, cross_origin
import json
import random
columns = ['vocab', 'Phonetic', 'Mean', 'Example']

from utils import make_response, preprocess_text, text_to_speech, addipa
# def text_to_speech(text):
#     name = text.replace(' ', '_')
    
#     # time.sleep(1) 
#     return f"./audio/{name}.mp3"

@app.route("/load_data/", methods=["POST"])
def load_data():
    start_time = time.time()
    csv_file = request.files['csv_file']
    df = pd.read_csv(csv_file).reset_index()
    print(time.time() - start_time)
    for col in columns:
        if col not in df.columns:
            return {"Status": "Please see format .csv with columns 'vocab', 'Phonetic', 'Mean', 'Example'"}, 401
    print("Start processing ")
    for i in df.index:
        start_time = time.time()
        vocab_ = df.vocab[i]
        if pd.isnull(vocab_):
            continue
        try:
            existing_vocab = vocab.query.filter_by(vocab=vocab_).one()
        except :
            existing_vocab = None
        
        
        mean_ = preprocess_text(df.Mean[i])
        example_ = preprocess_text(df.Example[i])
        phonetic_vocab_ = addipa(vocab_)
        phonetic_example_ = addipa(example_)
        audio_example_ = text_to_speech(example_)
        audio_vocab_ = text_to_speech(vocab_)
        if existing_vocab == None:
            print('oke')
            data = vocab(vocab=vocab_, phonetic_vocab=phonetic_vocab_, phonetic_example=phonetic_example_, 
                            mean=mean_, example=example_,
                            audio_example= audio_example_, audio_vocab = audio_vocab_)
            db.session.add(data)
            db.session.commit() 
        else:
            print('-----------')
            existing_vocab.phonetic_vocab = phonetic_vocab_
            existing_vocab.phonetic_example = phonetic_example_
            existing_vocab.mean = mean_
            existing_vocab.example = example_
            existing_vocab.audio_vocab = audio_vocab_
            existing_vocab.audio_example = audio_example_
            db.session.commit() 
        print(time.time() - start_time)
    print("Complete")
    return {'Status': 'Updata data successfull!'}, 200

@app.route("/generate-vocab/<path:randome>/", methods=["GET"])
@cross_origin()
def generate_vocab(randome):
    data = vocab.query.all()
    data_json = [ { 'vocab': item.vocab, 
                   'phonetic_example': item.phonetic_example, 
                   'phonetic_vocab': item.phonetic_vocab, 
                   'example': item.example, 
                   'mean': item.mean,
                   'audio_example': item.audio_example,
                   'audio_vocab': item.audio_vocab} for item in data]
    
    data_result = data_json.copy()
    if randome == 1 or randome == '1': 
        print("Vocab apply randome 1")
        data_result = random.shuffle(data_json)
        print(len(data_json))
    if randome == 2 or randome == '2': 
        print("Vocab apply randome 2")
        data_result = data_json[-20: ]
        data_result.reverse()
    if randome == 3 or randome == '3': 
        print("Vocab apply randome 3")
        half_part1 = data_json[: int(len(data_json)/2)]
        half_part2 = data_json[-int(len(data_json)/2) : ]
        
        random.shuffle(half_part1)
        random.shuffle(half_part2)
        
        data_result = half_part2[-10: ] + half_part1[:10 ]
        random.shuffle(data_result)


    return make_response(data_result), 200



@app.route("/add_data/", methods=["POST"])
@cross_origin()
def add_data():
    data = request.get_data(as_text=True)
    data_json = json.loads(data)
    vocab_ = preprocess_text(data_json['vocab'])
    mean_ = preprocess_text(data_json['mean'])
    example_ = preprocess_text(data_json['example'])
    if pd.isnull(vocab_):
        return {'Status': 'Vocab not empty!'}, 400
    if pd.isnull(mean_):
        return {'Status': 'Mean not empty!'}, 400
    if pd.isnull(example_):
        return {'Status': 'Example not empty!'}, 400
    
    try:
        existing_vocab = vocab.query.filter_by(vocab=vocab_).one()
    except :
        existing_vocab = None
    phonetic_vocab_ = addipa(vocab_)
    audio_vocab_ = text_to_speech(vocab_)
    
    phonetic_example_ = addipa(example_)
    audio_example_ = text_to_speech(example_)
    state = "Add word not complete"
    if existing_vocab == None:
        data = vocab(vocab=vocab_, phonetic_vocab=phonetic_vocab_, phonetic_example=phonetic_example_, 
                        mean=mean_, example=example_,
                        audio_example= audio_example_, audio_vocab = audio_vocab_)
        db.session.add(data)
        state = f"add {vocab_} successfull !" 
    else:
        existing_vocab.phonetic_vocab = phonetic_vocab_
        existing_vocab.phonetic_example = phonetic_example_
        existing_vocab.mean = mean_
        existing_vocab.example = example_
        existing_vocab.audio_vocab = audio_vocab_
        existing_vocab.audio_example = audio_example_
        state  = f"Update {vocab_} successfull !" 
    db.session.commit() 
    return {'Status': state}, 200
