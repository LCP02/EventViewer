from Event_Viewer import obter_eventos_por_tipo
from DataBase import consulta_servidor

def main():
    
    # Consultar a lista de servidores
    lista_servidores = consulta_servidor()
    
    # Para cada servidor, chamar a função obter_eventos_por_tipo
    for servidor in lista_servidores:

        obter_eventos_por_tipo('System',servidor)
        #obter_eventos_por_tipo('Security',servidor) 
        obter_eventos_por_tipo('Application',servidor)
        
if __name__ == "__main__":
    main()
