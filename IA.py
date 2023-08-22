import os
import requests
import json
from dotenv import load_dotenv
from DataBase import inserir_resposta_ia
from Gerenciador_Arquivos import log_conexao

def integracao_gpt(id_evento,tipo_log,mensagem_evento):
    
    try:
        
        api_key = os.environ.get('API_KEY')

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        link = "https://api.openai.com/v1/chat/completions"
        id_modelo = "gpt-3.5-turbo"
    
        body_menssagem = {
            "model": id_modelo,
            "messages":[
                {"role": "system", "content": "Olá, ChatGTP, você é um assistente de suporte."},
                {"role": "user", "content": f"Tenho um evento com o ID {id_evento} do tipo {tipo_log}, e com a mensagem: {mensagem_evento}, eu gostaria de saber qual é a causa desse evento e quais soluções devo seguir para resolvê-lo?"}  
            ]
        }
    
        body_menssagem = json.dumps(body_menssagem)
    
        requisicao = requests.post(link, headers=headers, data=body_menssagem)     
        print(requisicao)
        print(requisicao.text)
    
        resposta_json = requisicao.json()
        resposta_ia = resposta_json['choices'][0]['message']['content']
        inserir_resposta_ia(id_evento,resposta_ia)
    
    except Exception as erro:
        log_conexao(erro)
        
'''
import openai
from DataBase import inserir_resposta_ia

def integracao_gpt(id_evento, tipo_log, mensagem_evento):
    # Chave de API
    openai.api_key = "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"

    # Desabilitar a verificação SSL temporariamente
    openai.config.verify_ssl_certs = False

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Olá, ChatGTP, você é um assistente de suporte."},
            {"role": "user", "content": f"Tenho um evento com o ID {id_evento} do tipo {tipo_log}, e com a mensagem: {mensagem_evento}, eu gostaria de saber qual é a causa desse evento e quais soluções devo seguir para resolvê-lo?"}        ]
    )

    # Reabilitar a verificação SSL
    openai.config.verify_ssl_certs = True

    resposta_ia = response['choices'][0]['message']['content']
    inserir_resposta_ia(id_evento, resposta_ia)
 '''   
