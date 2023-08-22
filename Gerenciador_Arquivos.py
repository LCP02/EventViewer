import os
from datetime import datetime

def criar_pasta(servidor_log):
      
    caminho_pasta = f"\\\\{servidor_log}\\c$\\logs"
    
    try:
        if not os.path.exists(caminho_pasta):
            os.makedirs(caminho_pasta)
                            
    except:
        pass
    
    return caminho_pasta

def inserir_erro_em_arquivo(caminho_pasta, erro):
    try:
        # Definindo Caminho da Pasta + Nome do Arquivo
        caminho_arquivo = os.path.join(caminho_pasta, "Arquivo_Logs.txt")
        
        # Data e Hora atual
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Formatação da Menssagem
        mensagem = f"Data/Hora: {data_hora}\nErro: {erro}\n\n"

        # Verifica se o arquivo existe
        if not os.path.exists(caminho_arquivo):            
            with open(caminho_arquivo, 'w') as arquivo:  # Cria um novo arquivo vazio, no modo 'w' para escrita
                pass  # Pass não irá fazer nada no arquivo criado
          
        # Abre o arquivo no modo de adição ('a')
        with open(caminho_arquivo, 'a') as arquivo:
            arquivo.write(mensagem)
    
    except Exception as e:
        pass

def log_conexao(erro):
    servidor_log = 'CLBR397'
    caminho_pasta = criar_pasta(servidor_log)      
    if caminho_pasta:
        inserir_erro_em_arquivo(caminho_pasta, erro) 
    