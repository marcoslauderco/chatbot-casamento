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

def camel_case(s):
  s = str(s).lower()
  return ''.join([s[0].upper(), s[1:]])
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg').upper()
    tag = "Geral"
    if "BOM DIA" in userText or "BOA TARDE" in userText or "BOA NOITE" in userText or "OI" in userText or "OLÁ" in userText:
        tag = "Cumprimentos"
    if "QUANDO" in userText or ("DIA" in userText and "BOM DIA" not in userText) or "HORA" in userText:
        tag = "Quando"
    if "ONDE" in userText or "LOCAL" in userText or "CHEGAR" in userText or "CHEGO" in userText or "AONDE" in userText or "IR" in userText or "ENDEREÇO" in userText or "LOCALIZAÇÃO" in userText:
        tag = "Onde"
    
    resposta = chatbot.get_response(
        userText,
        additional_response_selection_parameters={
            'tags': [tag]
        }
    )
    return str(camel_case(resposta))

@app.route("/traine")
def get_bot_traine():
    chatbotTraine = ChatBot("Amazing Bot",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri="postgres://cehwxqvmrxdguy:c23e4da69da5277379a2d705b0cf5018471c362d767ae90cffe73e0309f643f7@ec2-3-224-125-117.compute-1.amazonaws.com:5432/dbru51gsii5r3a",
    read_only=False)
    trainer = ChatterBotCorpusTrainer(chatbotTraine)
    trainer.train("./corpus/greetings.yml")
    trainer.train("./corpus/quando.yml")
    trainer.train("./corpus/onde.yml")
    trainer.train("./corpus/casamento.yml")
    trainer.train("./corpus/compliment.yml")
    trainer.train("./corpus/conversations.yml")
    return str("Chatbot treinado")


if __name__ == "__main__":
    app.run()