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
  s = s.replace("lauder", "Lauder")
  s = s.replace("july", "July")
  s = s.replace("marcos", "Marcos")
  s = s.replace("juliani", "Juliani")
  s = s.replace("ilha d'capri", "Ilha d'Capri")
  s = s.replace("[endereco]", "Av. Paranavaí, 1733 - Pq. Ind. Bandeirantes. Maringá - PR")
  s = s.replace("[whatsapp]", "")
  s = s.replace("[diaehora]", "17 de Setembro de 2022 às 19:00")
  return ''.join([s[0].upper(), s[1:]])
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg').upper()
    userText = userText.replace("?", "")

    tag = "Geral"
    if "BOM DIA" in userText or "BOA TARDE" in userText or "BOA NOITE" in userText or "OI" in userText or "OLÁ" in userText:
        tag = "Cumprimentos"
    if "QUANDO" in userText or ("DIA" in userText and "BOM DIA" not in userText) or "HORA" in userText:
        return str(camel_case("DIA [diaehora]. POR FAVOR CHEGUE COM ANTECEDÊNCIA"))
    if "ONDE" in userText or "LOCAL" in userText or "AONDE" in userText:
        return str(camel_case("NO BUFFET ILHA D'CAPRI. A CERIMÔNIA E A FESTA SERÃO REALIZADAS NO MESMO LOCAL."))
    if "CHEGAR" in userText or "CHEGO" in userText or "IR" in userText or "ENDEREÇO" in userText or "LOCALIZAÇÃO" in userText:
        return str(camel_case("O BUFFET ILHA D'CAPRI FICA NA [endereco]"))
    if "ROUPA" in userText or "VESTIMENTA" in userText or "VESTIDO" in userText or "TERNO" in userText or "DRESS" in userText or "VESTIR" in userText:
        return str(camel_case("VISTA O MESMO QUE QUALQUER OUTRO CASAMENTO, TENHO CERTEZA QUE VOCÊ VAI ESTAR SHOW."))
    if "PRESENÇA" in userText:
        return str(camel_case("NÃO SE PREOCUPE A ASSESSORIA IRA ENTRAR EM CONTATO COM VOCÊ, MAS VOCÊ PODE TAMBÉM ENVIAR UMA MENSAGEM PARA O WHATSAPP DA ASSESORIA [whatsapp]"))
    if "PRESENTE" in userText or "PRESENTEAR" in userText or "PRESENTEIO" in userText:
        return str(camel_case("FELIZMENTE OS NOIVOS JÁ TEM TODA A CASA PRONTA, POR ESSE MOTIVO ELES PEDEM QUE SE POSSÍVEL VOCÊ DÊ SEU PRESENTE EM DINHEIRO (PIX OU LOJA DE PRESENTES)"))
    if "NOIVO" in userText or "NOIVA" in userText or "CASAL" in userText or "PADRINHO" in userText or "MADRINHA" in userText:
        tag = "noivos"
    if "BEBIDA" in userText or "COMIDA" in userText or "FRIOS" in userText or "CARDAPIO" in userText or "DRINK" in userText or "COMER" in userText or "BEBER" in userText or "DOCE" in userText or "BOLO" in userText or "SOBREMESA" in userText or "DOCINHO" in userText or "LANCHE" in userText or "JANTAR" in userText:
        tag = "comes"
    if "MUSICA" in userText or "BANDA" in userText or "DJ" in userText or "DANÇA" in userText or "DIVERSÃO" in userText:
        return str(camel_case("OS NOIVOS CONTRATARAM UM BANDA MANEIRA PARA ANIMAR A FESTA, EU JÁ ESTOU TREINANDO MEUS PASSOS DE DANÇA E VOCÊ?"))


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
    trainer.train("./corpus/vestimenta.yml")
    trainer.train("./corpus/presenca.yml")
    trainer.train("./corpus/presente.yml")
    trainer.train("./corpus/noivos.yml")
    trainer.train("./corpus/comes.yml")
    trainer.train("./corpus/diversao.yml")
    trainer.train("./corpus/casamento.yml")
    trainer.train("./corpus/compliment.yml")
    trainer.train("./corpus/conversations.yml")
    return str("Chatbot treinado")


if __name__ == "__main__":
    app.run()