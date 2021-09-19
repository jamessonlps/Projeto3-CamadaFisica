# Mensagem que client recebe do server quando o envio foi ok
SUCCESS = b'\xee\xee'*64

# Mensagem que client recebe do server quando o envio deu ruim
FAILURE = b'\xff\xff'*64

# Fixo e de livre escolha
EOP = b'\x00\xff\x0f\xf0'

FAILURE_COMMUNICATION = b'\xf0\x0f'*64
SUCCESS_COMMUNICATION = b'\x0f\xf0'*64
