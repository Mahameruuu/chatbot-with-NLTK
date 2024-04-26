import nltk
from nltk.chat.util import Chat, reflections
import mysql.connector
import json

nltk.download('punkt')

# Inisialisasi koneksi database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbot"
)
cursor = db_connection.cursor()

# Fungsi untuk menutup koneksi database
def close_database_connection():
    cursor.close()
    db_connection.close()

# Fungsi untuk menangani error pada koneksi database
def handle_database_error(error):
    print("Error occurred:", error)

# Fungsi untuk menyimpan percakapan ke database
def save_chat_to_database(user_input, bot_response):
    try:
        sql = "INSERT INTO chat_logs (user_input, bot_response) VALUES (%s, %s)"
        values = (user_input, bot_response)
        cursor.execute(sql, values)
        db_connection.commit()
    except mysql.connector.Error as err:
        handle_database_error(err)

# Fungsi untuk membaca data dari file JSON
def load_chat_data_from_json(file_path):
    with open(file_path, 'r') as file:
        chat_data = json.load(file)
    return chat_data

# Fungsi untuk menginisialisasi objek Chat
def initialize_chatbot(data):
    pairs = []
    for item in data:
        for pattern in item['pattern']:
            pairs.append((pattern, item['responses']))
    return Chat(pairs, reflections)

# Chatbot berinteraksi dengan pengguna
def chat_with_bot():
    print("Bot: Hai, ada yang bisa saya bantu?")
    while True:
        user_input = input("You: ")
        bot_response = chatbot.respond(user_input)
        print("Bot:", bot_response)
        save_chat_to_database(user_input, bot_response)
        if user_input.lower() == 'exit':
            break

# Load data chatbot dari file JSON
chat_data = load_chat_data_from_json('data/intents.json')
chatbot = initialize_chatbot(chat_data)

# Memulai percakapan dengan chatbot
chat_with_bot()

# Menutup koneksi database setelah selesai digunakan
close_database_connection()