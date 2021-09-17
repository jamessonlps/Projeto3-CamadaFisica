import time
import numpy         as np
from   src.enlace    import *
from   random        import randint
from   config.utils  import build_datagram
from   config.config import *

"""
Para verificar as portas no seu dispositivo:
    python -m serial.tools.list_ports
"""

#serialName = "/dev/ttyACM0"           # Ubuntu
#serialName = "/dev/tty.usbmodem1411"  # Mac
serialName = "COM7"                    # Windows


def main():
    try:
        start_communication = True    # Verdadeira enquanto o client não recebe resposta do protocolo de início do server
        sending_content = False       # Falsa enquanto o client não começar o envio dos dados
        
        # Cria objeto enlace
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação serial 
        com1.enable()
        print("Comunicação aberta com sucesso!")

        # Prepara todos os pacotes de dados a serem enviados
        datagrams, n_datagrams = build_datagram('small')

        # Protocolo de início: verifica se server responderá antes de
        # iniciar a transmissão de dados
        while start_communication:
            print("\nEnviando protocolo de início ao server")

            com1.sendData(SUCCESS_COMMUNICATION)
            print("\nTentativa de comunicação enviada. Aguardando server...")

            rxBeginResponse, nRxBeginResponse = com1.getData(2)
            time.sleep(0.05)

            if rxBeginResponse == FAILURE_COMMUNICATION:
                # Se o tempo estourar 5s e o dado não for completamente recebido,
                # usuário escolhe se começará novamente ou não
                print("\nTempo esgotado! Deseja tentar novamente? (s/n)")
                try_again = input()
                
                if try_again == 's' or try_again == 'S':
                    print("\nTentando comunicação novamente")
                
                elif try_again == 'n' or try_again == 'N':
                    print("\nEncerrando comunicação")
                    break

                else:
                    print("Comando inválido. Digitou errado porque quis, vou encerrar essa parada")
                    break

            # Se a resposta recebida for igual à enviada, segue para
            # a etapa do envio dos pacotes
            elif rxBeginResponse == SUCCESS_COMMUNICATION:
                print("\nComunicação com server estabelecida. Preparando envio de pacotes...")
                start_communication    = False
                sending_content        = True

            else:
                print("\nOcorreu algum erro, hein. Vamos tentar novamente")
                start_communication    = False

        last_pack = 0
        while sending_content:
            if last_pack < n_datagrams:
                print(f"\nEnviando pacote {last_pack+1} de {n_datagrams}...")
                # Faz envio do pacote
                com1.sendData(data=datagrams[last_pack])
                time.sleep(0.05)

                # Aguarda resposta do server se envio foi ok ou não
                response, n_response = com1.getData(2)
                time.sleep(0.05)

                if response == SUCCESS:
                    print(f"\nPacote {last_pack+1} de {n_datagrams} enviado com sucesso")
                    last_pack += 1
                
                elif response == FAILURE:
                    print(f"\nErro ao enviar pacote {last_pack+1}. Preparando reenvio...")
                
                else:
                    print(f"\nOcorreu um erro inesperado na comunicação. Reenviando pacote {last_pack+1}")

            else:
                print("\nTodos os pacotes foram enviados com sucesso!")
                print("Fechando comunicação")
                sending_content = False

        com1.disable()
        print(f"\nComunicação encerrada")

    except KeyboardInterrupt:
        print("Fechamento forçado")
        com1.disable()
        
    except Exception as erro:
        print("Ocorreu um erro na execução:\n")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
