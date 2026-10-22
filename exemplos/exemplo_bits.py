import sys
import os
from time import sleep

# Adiciona o diretório raiz ao path para conseguir importar a pasta cliente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cliente.clientemodbus import ClienteMODBUS

def executar_demonstracao_bits():
    # Inicializa o cliente (ajuste o IP e porta conforme o seu servidor)
    cliente = ClienteMODBUS('127.0.0.1', 502)
    
    if cliente.conectar():
        print("Conectado ao servidor MODBUS com sucesso!")
        endereco_comando = 1300 # Endereço do Battery_Enable da sua tabela
        bit_alvo = 0            # Vamos usar o bit 0 para este comando
        
        # 1. Preparação: Escreve um valor inicial com outros bits já ativados
        # O número 42 em binário é 0000000000101010 (bits 1, 3 e 5 ativados)
        print(f"\n[Etapa 1] Inserindo valor inicial no registrador {endereco_comando}...")
        cliente.escreveDado(1, endereco_comando, 42) 
        sleep(1)
        
        # 2. Leitura inicial dos 16 bits
        print("\n[Etapa 2] Leitura Inicial:")
        bits_iniciais = cliente.ler_bits_registrador(endereco_comando)
        print(f"Estado dos 16 bits: {bits_iniciais}")
        
        # 3. Alterar apenas o bit alvo para 1
        print(f"\n[Etapa 3] Alterando o bit {bit_alvo} para 1...")
        cliente.escrever_bit_individual(endereco_comando, bit_alvo, 1)
        bits_apos_1 = cliente.ler_bits_registrador(endereco_comando)
        print(f"Novo estado:        {bits_apos_1}")
        
        # 4. Alterar apenas o bit alvo para 0
        print(f"\n[Etapa 4] Alterando o bit {bit_alvo} para 0...")
        cliente.escrever_bit_individual(endereco_comando, bit_alvo, 0)
        bits_apos_0 = cliente.ler_bits_registrador(endereco_comando)
        print(f"Novo estado:        {bits_apos_0}")
        
        print("\nDemonstração concluída! Observe que os bits 1, 3 e 5 permaneceram inalterados.")
        
        cliente.fechar()
    else:
        print("Falha ao conectar no servidor. Verifique se ele está em execução.")

if __name__ == '__main__':
    executar_demonstracao_bits()