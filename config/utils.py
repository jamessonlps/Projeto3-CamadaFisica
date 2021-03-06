import numpy         as np
from   config.config import EOP

def build_head(pack_number:int, len_package:int, len_payload:int):
    """
        Constrói o HEAD do pacote, em que os dois primeiros
        bytes correspondem ao número do pacote e os 2 últimos
        dá o número total de pacotes sendo transmitidos
    """
    pack_id     = pack_number.to_bytes(2, byteorder='little')
    package_len = len_package.to_bytes(2, byteorder='little')
    payload_len = len_payload.to_bytes(2, byteorder='little')
    
    return b''.join([pack_id, b'\xee'*4, payload_len, package_len])



def number_of_packs(len_bytes, max_size=114):
    """
        Recebe o total de bytes que o arquivo contém e retorna
        quantos pacotes serão montados com o limite de até {max_size}
    """
    
    prop = len_bytes // max_size
    n    = int(len_bytes / max_size)
    if prop == 0:
        return n
    else:
        return n + 1



def build_datagram(file_name, max_size=114):
    """
        Recebe o arquivo a ser enviados e constrói todos os pacotes
        necessários para que o client o envie ao server, retornando
        o conjunto de pacotes e o número total de pacotes
    """

    # Carrega arquivo em bytes
    with open (f'img/{file_name}.png', 'rb') as file:
        content = file.read()
        bytes_content = bytearray(content)
    
    packages = list()
    
    # Número de pacotes a serem enviados
    len_packs = number_of_packs(len(bytes_content))
    
    # Constrói cada datagrama e preenche a lista de pacotes
    for i in range(0, len_packs):
        if i == len_packs - 1:
            pack = bytes_content[ i*max_size : -1 ]
        else:
            pack = bytes_content[ i*max_size : (i+1)*max_size ]
        # Constrói o head
        head = build_head(pack_number=i, len_package=len_packs, len_payload=len(pack))
        
        if len(pack) < 114:
            pack = b''.join([pack, b'\x00'*(114 - len(pack))])
        
        # Monta o datagrama
        datagram = b''.join([head, pack, EOP])
        packages.append(datagram)

    return packages, len_packs



def extract_pack_info(package:bytes):
    """
        Retorna o número do pacote e o EOP ao final do
        datagrama recebido pelo server
    """
    pack_id     = package[:2]
    len_payload = (package[6:8])
    total_packs = package[8:10]
    payload     = package[10:10+int.from_bytes(len_payload, 'little')]
    eop         = package[-4:]

    return pack_id, total_packs, payload, len_payload, eop
