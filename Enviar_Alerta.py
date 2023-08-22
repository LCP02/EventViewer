import os
import smtplib
import ssl
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Gerenciador_Arquivos import log_conexao


def enviar_email(id_evento, tipo_log ,data_evento, server_evento, mensagem_evento):
    try:
        
        # Configurações do servidor de e-mail
        servidor_smtp = os.environ.get('SMTP_SERVER')
        smtp_porta = int(os.environ.get('SMTP_PORT'))
        usuario_smtp = os.environ.get('SMTP_USER')
        senha_smtp = os.environ.get('SMTP_PASSWORD')
        remetente_email = os.environ.get('SENDER_EMAIL')
        destinatario_email = os.environ.get('RECIPIENT_EMAIL')
        
        assunto = f"ALERTA: Evento com ID {id_evento} encontrado em {server_evento}"
        body = f"Evento {id_evento} tipo {tipo_log} encontrado no servidor {server_evento}, {data_evento}, Menssagem: {mensagem_evento}"

        # Criando a mensagem
        msg = MIMEMultipart()
        msg['From'] = remetente_email
        msg['To'] = destinatario_email
        msg['Subject'] = assunto
        
        # Adicionando o corpo da mensagem
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Crie um contexto SSL com a versão TLS 1.2
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')  # Configuração adicional para forçar TLS 1.2

        with smtplib.SMTP(servidor_smtp, smtp_porta) as server:
            server.starttls(context=context)  # Use starttls() se estiver usando a porta 587 (TLS/STARTTLS)
            server.login(usuario_smtp, senha_smtp)
            server.sendmail(remetente_email, destinatario_email, msg.as_string())
    
    except Exception as erro:
        log_conexao(erro)
                 
'''        
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do servidor de e-mail
servidor_smtp = 'smtp.office365.com'
smtp_porta = 587  # Usar 587 para TLS ou STARTTLS, ou 465 para SSL
remetente_email = 'meugrupo@email.com'
destinatario_email = 'destinatario@email.com'

# Criar objeto do e-mail
mensagem = MIMEMultipart()
mensagem['From'] = remetente_email
mensagem['To'] = destinatario_email
mensagem['Subject'] = 'Assunto do e-mail'

# Corpo do e-mail
mensagem_corpo = 'Conteúdo do e-mail aqui.'
mensagem.attach(MIMEText(mensagem_corpo, 'plain'))

# Enviar o e-mail
server = smtplib.SMTP(servidor_smtp, smtp_porta)
# Caso seu servidor exija autenticação, descomente as linhas abaixo:
# server.login(usuario_smtp, senha_smtp)
server.sendmail(remetente_email, destinatario_email, mensagem.as_string())
server.quit()
'''