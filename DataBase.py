import os
import pymongo
from Gerenciador_Arquivos import log_conexao 
from dotenv import load_dotenv
 
    
def cofiguração_database():
    try:
        
        nome_servidor = os.environ.get('MONGO_DB_HOST')
        porta_servidor = int(os.environ.get('MONGO_DB_PORT'))
        nome_banco_dados = os.environ.get('MONGO_DB_NAME')

        # Estabelecendo a conexão com o banco de dados MongoDB
        cliente = pymongo.MongoClient(f'mongodb://{nome_servidor}:{porta_servidor}/')
        banco_dados = cliente[nome_banco_dados]
        
        return banco_dados, cliente
    
    except pymongo.errors.PyMongoError as erro:
        
        log_conexao(erro)
        
def consulta_lista(id_evento):
    try:
        
        banco_dados, cliente = cofiguração_database() #Chama Função com parametros de conexão
        tipo = 'BlackList' # Seta variavel tipo como BlackList
        colecao_listas = banco_dados['Listas'] # Indica Colletion para verificação
        
        # Buscar documentos com o id_evento desejado
        resultado = colecao_listas.find({'id_evento': id_evento, 'tipo': tipo}) # Realiza a consulta com parametros id_evento e tipo

        if resultado is not None:                
            return True # Se ID estiver na colletion retornar Verdadeiro
  
    except pymongo.errors.PyMongoError as erro:

        log_conexao(erro) #Insere erro caso exista
            
    finally:         
        cliente.close()  # Fechando a conexão com o banco de dados MongoDB  

def consulta_servidor():
    try:

        banco_dados, cliente = cofiguração_database()

        # Obtendo a coleção onde iremos inserir o documento (registro)
        colecao_servidores = banco_dados['Servidores']

        # Consultar e retornar a lista de servidores
        servidores = colecao_servidores.find({}, {"_id": 0, "nome_servidor": 1})  # Excluindo o campo _id e incluindo apenas o campo nome
        lista_servidores = [servidor['nome_servidor'] for servidor in servidores]
        
        return lista_servidores
    
    except pymongo.errors.PyMongoError as erro:

        log_conexao(erro)
            
    finally:         
        cliente.close()  # Fechando a conexão com o banco de dados MongoDB  
       
def inserir_evento(tipo_log, id_evento, categoria_evento, tipo_evento, data_evento, fonte_evento, server_evento, mensagem_evento):
    try:

        banco_dados, cliente = cofiguração_database()

        # Obtendo a coleção onde iremos inserir o documento (registro)
        colecao_logs = banco_dados['Logs_Event']

        # Criando um dicionário (documento) com os dados do evento
        evento = {
            'tipo_log': tipo_log,
            'id_evento': id_evento,
            'categoria': categoria_evento,
            'tipo': tipo_evento,
            'data': data_evento,
            'fonte': fonte_evento,
            'server': server_evento,
            'msg_evento': mensagem_evento
        }

        # Inserindo o evento na coleção
        colecao_logs.insert_one(evento)
    
    except pymongo.errors.PyMongoError as erro:

        log_conexao(erro)
            
    finally:         
        cliente.close()  # Fechando a conexão com o banco de dados MongoDB
        
def inserir_resposta_ia(id_evento,resposta_ia):
    try:

        banco_dados, cliente = cofiguração_database()

        # Obtendo a coleção onde iremos inserir o documento (registro)
        colecao_logs = banco_dados['Analise_IA']

        # Criando um dicionário (documento) com os dados do evento
        resposta = {
            'ID Evento':id_evento,
            'Resposta': resposta_ia       
        }

        # Inserindo o evento na coleção
        colecao_logs.insert_one(resposta)
    
    except pymongo.errors.PyMongoError as erro:

        log_conexao(erro)
            
    finally:         
        cliente.close()  # Fechando a conexão com o banco de dados MongoDB
   
