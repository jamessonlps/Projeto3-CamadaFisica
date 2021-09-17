import time
import numpy  as np
from   enlace import *
from   config import SUCCESS, FAILURE, EOP
from   utils  import extract_pack_info

"""
Para verificar as portas no seu dispositivo:
    python -m serial.tools.list_ports
"""

#serialName = "/dev/ttyACM0"           # Ubuntu
#serialName = "/dev/tty.usbmodem1411"  # Mac
serialName = "COM8"                    # Windows


waiting_contact = True # Verdadeira enquanto aguarda contato de um client
receiving_data  = False
building_file   = False

async def main():
    try:
        # Inicializando porta do server
        com2 = enlace(serialName)
        com2.enable()
        print("\nComunicação inicializada")

        while waiting_contact:
            print("\nAguardando client...")
            # Aguarda contato do client
            rxBufferBegin, nRxBufferBegin = await com2.getData(3)

            # Reenvia ao client o protocolo de início recebido
            com2.sendData(rxBufferBegin)
            print("\nContato com client estabelecido. Iniciando recepção...")
            waiting_contact = False
            receiving_data  = True

        now_pack = 0 # pacote que o server espera receber
        full_data = []
        while receiving_data:
            
            # Recebimento do pacote
            pack_response, n_pack_response = await com2.getData(size=128)

            if n_pack_response == 128:
                # Extrai número do pacote, total e o EOP
                pack_id, total_packs, payload, eop = extract_pack_info(pack_response)
                
                # Verifica se o pacote recebido e o EOP são os esperados
                if pack_id == now_pack and eop == EOP:
                    print(f"\nPacote {pack_id+1} de {total_packs} recebido")
                    full_data.append(payload)
                    com2.sendData(SUCCESS)
                    now_pack += 1
                    
                    # Se o próximo pack for igual ao total de packs, se encerra a recepção
                    if now_pack == total_packs:
                        print("\nTodos os pacotes foram recebidos")
                        receiving_data = False
                        building_file  = True
                
                else:
                    print("\nPacote errado. Solicitando novamente o pacote ao client")
                    # Envia mensagem para sinalizar erro para o client para que 
                    # ele reenvie o pacote com problemas na recepção
                    com2.sendData(FAILURE)

        while building_file:
            data_bytes = b''.join([pack for pack in full_data])
            with open('img/uhuuu.png', 'wb') as file:
                file.write(data_bytes)
                print("\nArquivo salvo com sucesso!")

        com2.disable()
        print("Comunicação encerrada.")

        
    except Exception as erro:
        print("Ocorreu um erro na execução:\n")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
