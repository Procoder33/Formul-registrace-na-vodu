from flask import Flask, render_template, request
import re
import json

app = Flask(__name__)

DATA_FILE = 'seznam_registrace.json'




def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return data if data else []
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

registration_list = load_data()

@app.route('/')
def mainpage():
    return render_template('prvni_stranka.html', ucastnici = registration_list), 200

@app.route('/druha_stranka', methods=['GET'])
def secondpage():
    return render_template('druha_stranka.html', zprava="Tajná zpráva.."), 200

@app.route('/registrace', methods=['GET', 'POST'])
def thirdpage():
    global registration_list

    if request.method == 'POST':
        name_pattern = re.compile(r'([A-Za-z0-9]+)\S')
        is_swimmer = request.form['is_swimmer']
        first = request.form['firstName']
        last = request.form['lastName']
        classr = request.form['class']
        friend_name = request.form['friend_to_go_with']

        if is_swimmer == 'Ano':
            registration_list.append({'firstname': first, 'lastname': last, 'class': classr, 'is_swimmer': is_swimmer, 'friend_name': friend_name})
            save_data(registration_list)  # Uložení dat po úspěšné registraci
            print('Všechno je v pořádku.')
            return render_template('prvni_stranka.html', ucastnici = registration_list), 200

        else:
            print('Nesprávně zadané údaje, nebo nesplněné podmínky!')
            return render_template('registrace.html',alert_message='Nesprávně zadané údaje, nebo požadavek není splněn !'), 400

    return render_template('registrace.html'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
