from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

DATA_BASE = pd.read_csv("backend\\TO_DO_LIST\\DATA.csv", sep=';', encoding='utf-8')

def save_data(data):
    data.to_csv("backend\\TO_DO_LIST\\DATA.csv", sep=';', index=False, encoding='utf-8')

def all_text_to_do(data):
    text = data['текст'].tolist()
    return text

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api', methods=['GET'])        # просто api со всеми делами в одной строке
def data_1():
    text = all_text_to_do(DATA_BASE)
    message = ""
    for i in range(len(text)):
        message += str(i + 1) + ")" + text[i] + ","
    return jsonify({'mes': message}), 200

@app.route('/api/send', methods=['POST'])    # Если пользователь ввёл текст
def data_2():
    user_text = request.form.get('text')  # Получаем текст от пользователя
    user_text = user_text.strip().lower()
    if user_text == "чит код":
        return jsonify({'response': "Сегодня можно и отдохнуть"}), 200
    
    # Добавление новой задачи в DataFrame
    else:
        new_task = pd.DataFrame({'текст': [user_text], 'статус': [0], 'важность': [1], 'время добавления': [pd.Timestamp.now()]})
        global DATA_BASE
        DATA_BASE = pd.concat([DATA_BASE, new_task], ignore_index=True)
        save_data(DATA_BASE)
        return jsonify({'response': "Задача добавлена."}), 200


@app.route('/api/delete', methods=['POST'])    # удаление
def delete_task():
    user_text = request.form.get('text')
    global DATA_BASE
    DATA_BASE = DATA_BASE[DATA_BASE['текст'] != user_text[2:]]
    save_data(DATA_BASE)
    return jsonify({'response': "Задача удалена."}), 200

@app.route('/api/edit', methods=['POST'])
def edit_task():
    old_text = request.form.get('old_text')
    new_text = request.form.get('new_text')
    global DATA_BASE
    DATA_BASE.loc[DATA_BASE['текст'] == old_text[2:], 'текст'] = new_text
    save_data(DATA_BASE)
    return jsonify({'response': "Задача обновлена."}), 200


if __name__ == '__main__':
    app.run(debug=True)
    