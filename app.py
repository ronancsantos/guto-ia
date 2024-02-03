from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo"

app = Flask(__name__)
app.secret_key = '@iemanoguto'

contexto = carrega("dados/ecomart.txt")


def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0

    while True:
        try:
            prompt_do_sistema = f"""
            Você é um chatbot de atendimento a clientes de um e-commerce. 
            Você não deve responder perguntas que não sejam dados do e-commerce informado!
            
            Você deve gerar respostas utilizando o contexto abaixo
            
            # Contexto
            {contexto}
            """

            response = cliente.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_do_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model=modelo
            )

            return response.choices[0].message.content
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                raise Exception("Erro no GPT: %s" % erro)
            print('Erro de comunicação com OpenAI:', erro)
            sleep(1)


@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    try:
        resposta = bot(prompt)
        return resposta
    except Exception as erro:
        return "Erro no chatbot: %s" % erro

#Rota principal
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
