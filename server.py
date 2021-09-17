import time
import numpy  as np
from   enlace import *
from   config import *
from   utils  import extract_pack_info

"""
Para verificar as portas no seu dispositivo:
    python -m serial.tools.list_ports
"""

#serialName = "/dev/ttyACM0"           # Ubuntu
#serialName = "/dev/tty.usbmodem1411"  # Mac
serialName = "COM8"                    # Windows


def main():
    waiting_contact = True # Verdadeira enquanto aguarda contato de um client
    receiving_data  = False
    building_file   = False
    
    try:
        # Inicializando porta do server
        com2 = enlace(serialName)
        com2.enable()
        print("\nComunicação inicializada")

        while waiting_contact:
            print("\nAguardando client...")
            # Aguarda contato do client
            rxBufferBegin, nRxBufferBegin = com2.getData(2)
            time.sleep(0.05)

            if rxBufferBegin == SUCCESS_COMMUNICATION:
                # Reenvia ao client o protocolo de início recebido
                com2.sendData(rxBufferBegin)
                time.sleep(0.05)
                print("\nContato com client estabelecido. Iniciando recepção...")
                waiting_contact = False
                receiving_data  = True
            
            else:
                print("\nOcorreu uma falha na comunicação.")

        now_pack = 0 # pacote que o server espera receber
        full_data = []
        while receiving_data:
            
            # Recebimento do pacote
            pack_response, n_pack_response = com2.getData(size=128)
            time.sleep(0.05)

            # Extrai número do pacote, total, dados e o EOP
            pack_id, total_packs, payload, len_payload, eop = extract_pack_info(pack_response)


            pack_id_int = int.from_bytes(pack_id, 'little')
            len_payload_int = int.from_bytes(len_payload, 'little')

            
            # Verifica se o pacote recebido e o EOP são os esperados
            if pack_id_int == now_pack and eop == EOP and len_payload_int == len(payload):
                print(f"\nPacote {pack_id_int+1} de {int.from_bytes(total_packs, 'little')} recebido")
                full_data.append(payload)
                com2.sendData(SUCCESS)
                
                now_pack += 1

                # Se o próximo pack for igual ao total de packs, se encerra a recepção
                if now_pack == int.from_bytes(total_packs, 'little'):
                    print("\nTodos os pacotes foram recebidos")
                    receiving_data = False
                    building_file  = True
                
            
            else:
                if pack_id_int != now_pack:
                    print(f"\nPacote {pack_id_int} recebido ao invés de {now_pack}. Solicitando novamente o pacote certo")
                elif len_payload != len(payload):
                    print(f"\nPacote {now_pack+1} recebido com payload diferente do informado")
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
            building_file = False

        com2.disable()
        print("Comunicação encerrada.")

    except KeyboardInterrupt:
        print("\nPrograma fechado a força")
        com2.disable()
        
    except Exception as erro:
        print("Ocorreu um erro na execução:\n")
        print(erro)
        com2.disable()

        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
