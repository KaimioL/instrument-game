from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

instruments = [
    {"name": "Guitar", "image": "https://fast-images.static-thomann.de/pics/bdb/_13/130180/17136473_800.jpg"},
    {"name": "Piano", "image": "https://fi.yamaha.com/fi/files/b3-SC2_a_1001_972885e0382a20ca6bc0a105b33b79b6.jpg?impolicy=resize&imwid=2000&imhei=1815"},
    {"name": "Banjo", "image": "https://d1aeri3ty3izns.cloudfront.net/media/90/900544/600/preview.jpg"},
    {"name": "Flute", "image": "https://thumbs.static-thomann.de/thumb/padthumb600x600/pics/bdb/_31/317787/7168995_800.jpg"},
    {"name": "Cello", "image": "https://thumbs.static-thomann.de/thumb/padthumb600x600/pics/bdb/_47/472845/15009745_800.jpg"},
    {"name": "Accordion", "image": "https://thumbs.static-thomann.de/thumb/padthumb600x600/pics/bdb/_51/513157/16523071_800.jpg"},
]

@app.route('/')
def index():
    instruments_sample = random.sample(instruments, 4)

    return render_template('index.html', instruments = instruments_sample, correct_answer = random.choice(instruments_sample))

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = request.form['answer']
    correct_answer = request.form['correct_answer']
    if user_answer == correct_answer:
        result = "Correct! Well Done!"
    else:
        result = f"Wrong :( Correct anser was {correct_answer}"
    
    instruments_sample = random.sample(instruments, 4)

    return jsonify({'result': result, 'next_instruments': [x['name'] for x in instruments_sample], 'next_correct_answer': random.choice(instruments_sample)})