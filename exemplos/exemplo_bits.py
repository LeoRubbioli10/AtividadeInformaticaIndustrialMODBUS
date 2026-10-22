import sys
import os
from time import sleep

# Adiciona o diretório raiz ao path para conseguir importar a pasta cliente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cliente.clientemodbus import ClienteMODBUS