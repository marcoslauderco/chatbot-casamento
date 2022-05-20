from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

chatbot = ChatBot("Amazing Bot",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri="postgres://svuhlvfubmlwoa:33e69316cac0b35f5bb9f4844d9304d841da64250709015c12da7ad3142c4520@ec2-52-86-115-245.compute-1.amazonaws.com:5432/d4756h8ddhd1fs")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("./corpus/casamento.yml")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.generate_response(userText))


if __name__ == "__main__":
    app.run()