# Mensagem que client recebe do server quando o envio foi ok
SUCCESS = b'\xee\xee'

# Mensagem que client recebe do server quando o envio deu ruim
FAILURE = b'\xff\xff'

# Fixo e de livre escolha
EOP = b'\x00\xFF\x0F\xF0'
