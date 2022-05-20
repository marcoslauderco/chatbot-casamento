from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

chatbot = ChatBot("Amazing Bot",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri="postgres://cehwxqvmrxdguy:c23e4da69da5277379a2d705b0cf5018471c362d767ae90cffe73e0309f643f7@ec2-3-224-125-117.compute-1.amazonaws.com:5432/dbru51gsii5r3a",
    read_only=True)
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train("./corpus/casamento.yml")
# trainer.train("./corpus/compliment.yml")
# trainer.train("./corpus/conversations.yml")
# trainer.train("./corpus/greetings.yml")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))


if __name__ == "__main__":
    app.run()