import win32evtlog 
import win32evtlogutil
#import winerror
#import socket
from datetime import datetime
from DataBase import inserir_evento
from Enviar_Alerta import enviar_email
from IA import integracao_gpt 

# Função para formatar Id do Evento para Decimal 
def formatar_IdEvento(id_evento):   
    if id_evento < 0: #Verificar se o ID do evento é negativo e converte para inteiro
        id_evento = id_evento & 0xFFFFFFFF
    idEvento_ajustado = id_evento & 0x3FFF  # 0x3FFF é o valor fixo para ajustar o ID para o valor correto
    return idEvento_ajustado
    
#Função para converter Data do Evento
def formatar_tempo_evento(tempo_evento):
    hora_formatada = datetime.strptime(tempo_evento, "%a %b %d %H:%M:%S %Y") # Converter o tempo do evento
    return hora_formatada.strftime("%Y-%m-%d %H:%M:%S")

#Função para obter informações do Event Viewer
def obter_eventos_por_tipo(tipo_log,servidor):
    from DataBase import consulta_lista
    # Informações para conexão ao EventViewer 
    #servidor = socket.gethostname() # Obter o nome do computador local  
    identificador_log = win32evtlog.OpenEventLog(servidor, tipo_log) # Parametros de Nome Servidor e Tipo do Evento (System,Security,Application)
    tamanho_pagina = 1000 # Tabulação em blocos de 1000
    indice_evento = 0 # Inicio da leitura
    
    while True:
        
        tipo_leitura = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ # Definindo o tipo_leitura de leitura do log de eventos

        # Lendo os eventos do log
        eventos = win32evtlog.ReadEventLog(identificador_log, tipo_leitura, indice_evento, tamanho_pagina)

        if not eventos:
            break
        
        for evento in eventos:
            id_evento = formatar_IdEvento(evento.EventID)
            categoria_evento = evento.EventCategory
            tipo_evento = evento.EventType      
            data_evento = formatar_tempo_evento(evento.TimeGenerated.Format())
            fonte_evento = evento.SourceName
            server_evento = evento.ComputerName
            mensagem_evento = win32evtlogutil.SafeFormatMessage(evento, tipo_log)   
                   
        # Verificar se o evento é de nível '[1]Erro' ou '[2]Aviso'
        if tipo_evento == 1 or tipo_evento == 2:           
            consulta_lista_resultado = consulta_lista(id_evento) #Consulta se o ID está na BlackList
            if consulta_lista_resultado: # Se o ID estiver na BlackList segue...
                enviar_email(id_evento, tipo_log ,data_evento, server_evento, mensagem_evento) # Envia um email de alerta
                integracao_gpt(id_evento,tipo_log,mensagem_evento) # Integra via API com a Openai, para obter informalções do erro
                
            inserir_evento(tipo_log, id_evento, categoria_evento, tipo_evento, data_evento, fonte_evento, server_evento, mensagem_evento)  # Chamar a função para inserir o evento no banco de dados
                
    
        # Atualizar o índice para a próxima leitura
        indice_evento += len(eventos)    
  
    # Fechando o log de eventos
    win32evtlog.CloseEventLog(identificador_log)