import nltk
from nltk.chat.util import Chat, reflections
import mysql.connector
import json
import pandas as pd

nltk.download('punkt')

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbot"
)
cursor = db_connection.cursor()

# read data and respons from JSON
def load_chat_data_from_json(file_path):
    with open(file_path, 'r') as file:
        chat_data = json.load(file)
    return chat_data

def initialize_chatbot(data):
    pairs = []
    for item in data:
        for pattern in item['pattern']:
            pairs.append((pattern, item['responses']))
    return Chat(pairs, reflections)

# save speak to database MySQL
def save_chat_to_database(user_input, bot_response):
    sql = "INSERT INTO chat_logs (user_input, bot_response) VALUES (%s, %s)"
    values = (user_input, bot_response)
    cursor.execute(sql, values)
    db_connection.commit()

# read data chatbot from file JSON
chat_data = load_chat_data_from_json('data/intents.json')
chatbot = initialize_chatbot(chat_data)

def chat_with_bot():
    print("Bot: Hai, ada yang bisa saya bantu?")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Bot: Sampai jumpa lagi!")
            break

        # Identifikasi jika pengguna mengirim pesan marah
        if 'marah' in user_input.lower() or 'kesal' in user_input.lower() or 'ngamuk' in user_input.lower():
            bot_response = "Maaf jika ada yang membuat Anda marah. Saya di sini untuk membantu. Ada yang bisa saya lakukan?"
        else:
            bot_response = chatbot.respond(user_input)

        print("Bot:", bot_response)
        save_chat_to_database(user_input, bot_response)

chat_with_bot()