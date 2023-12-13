from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

instruments = [
    {"name": "Guitar", "image": "https://fast-images.static-thomann.de/pics/bdb/_13/130180/17136473_800.jpg"},
    {"name": "Piano", "image": "https://fi.yamaha.com/fi/files/b3-SC2_a_1001_972885e0382a20ca6bc0a105b33b79b6.jpg?impolicy=resize&imwid=2000&imhei=1815"},
    {"name": "Banjo", "image": "https://d1aeri3ty3izns.cloudfront.net/media/90/900544/600/preview.jpg"},
    {"name": "Hang Drum", "image": "https://play-lh.googleusercontent.com/eqCpzmemdiOSPZTb07lwgNR3YQYTKcs1511nQiEz6K1fR6iXl6CW-26iJpYpjsZ3KIo"},
    {"name": "Crwth", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Crwth_rem.jpg/1200px-Crwth_rem.jpg"},
    {"name": "Glass Armonica", "image": "https://benjaminfranklinhouse.org/wp-content/uploads/2018/03/instrument-angled_p70-1030x686.jpg"},
    {"name": "Totem Harp", "image": "https://www.instrmnts.com/wp-content/uploads/2018/11/toha-instrmnts-exhibition-victor-gama.jpg"},
    {"name": "Stylophone", "image": "https://thumbs.static-thomann.de/thumb/padthumb600x600/pics/bdb/_49/494702/16251321_800.jpg"},
    {"name": "Theremin", "image": "https://www.soitinlaine.fi/media/catalog/product/cache/74daeb03f7d343fc5ee431e800bde6c5/c/a/catalog_MOOG_Etherwave_Partner-6.jpg"},
    {"name": "Cimbalom", "image": "https://dms-cf-01.dimu.org/image/022yjV2nwfED?dimension=800x800"},
]

@app.route('/')
def index():
    instruments_sample = random.sample(instruments, min(len(instruments), 4))

    return render_template('index.html', instruments = instruments_sample, correct_answer = random.choice(instruments_sample))

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = request.form['answer']
    correct_answer = request.form['correct_answer']
    guessed_instruments = int(request.form['guessed_instruments'])

    # Add previous instrument to binary of already guessed instruments
    for i, instrument in enumerate(instruments):
        if instrument['name'] == correct_answer:
            guessed_instruments += 2**i

    instruments_left = instruments.copy()

    # Create list of instruments left
    guessed_instruments_list = [int(i) for i in bin(guessed_instruments)[2:]]
    guessed_instruments_list.reverse()

    for i, val in reversed(list(enumerate(guessed_instruments_list))):
        if bool(val):
            del instruments_left[i]

    if not instruments_left:
        result = "All instruments guessed! Game over"
        return jsonify({'result': result, 'next_instruments': [], 'next_correct_answer': "", 'guessed_instruments': 0})

    elif user_answer == correct_answer:
        result = "Correct! Well Done!"
    else:
        result = f"Wrong :( Correct anser was {correct_answer}"

    instruments_sample = random.sample(instruments, min(len(instruments), 3))

    return jsonify({'result': result, 'next_instruments': [x['name'] for x in instruments_sample], 'next_correct_answer': random.choice(instruments_sample), 'guessed_instruments': guessed_instruments})

@app.route('/add_instrument', methods=['POST'])
def add_instrument():
    data = request.json

    if data.get('name') == None:
        return "Instrument data is missing name"
    elif data.get('image') == None:
        return "Instrument data is missing image link"
    
    instruments.append({'name': data.get('name'), 'link': data.get('link')})

    return f"{data.get('name')} added"