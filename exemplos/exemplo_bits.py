import sys
import os
from time import sleep

# Adiciona o diretório raiz ao path para conseguir importar a pasta cliente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ClienteMODBUS.clientemodbus import ClienteMODBUS

def executar_demonstracao_bits():
    # Inicializa o cliente (ajuste o IP e porta conforme o seu servidor)
    cliente = ClienteMODBUS('127.0.0.1', 502)
    
    if cliente.conectar():
        print("Conectado ao servidor MODBUS com sucesso!")
        endereco_comando = 1300  # Endereço do registrador de comando
        bit_alvo = 0             # Vamos usar o bit 0 para este comando

        # 1. Preparação: Escreve um valor inicial com outros bits já ativados
        # O número 42 em binário é 0000000000101010 (bits 1, 3 e 5 ativados)
        print(f"\n[Etapa 1] Inserindo valor inicial no registrador {endereco_comando}...")

        if not cliente.escreveDado(1, endereco_comando, 42):
            print("Falha ao inicializar o registrador.")
            cliente.fechar()
            return

        # 2. Leitura inicial dos 16 bits
        print("\n[Etapa 2] Leitura Inicial:")
        bits_iniciais = cliente.ler_bits_registrador(endereco_comando)

        if bits_iniciais is None:
            print("Falha ao ler os bits do registrador.")
            cliente.fechar()
            return

        for i, bit in enumerate(bits_iniciais):
            print(f"Bit {i}: {bit}")

        # 3. Alterar apenas o bit alvo para 1
        print(f"\n[Etapa 3] Alterando o bit {bit_alvo} para 1...")

        if not cliente.escrever_bit_individual(endereco_comando, bit_alvo, 1):
            print("Falha ao ativar o bit.")
            cliente.fechar()
            return

        bits_apos_1 = cliente.ler_bits_registrador(endereco_comando)
        print(f"Novo estado: {bits_apos_1}")

        # 4. Alterar apenas o bit alvo para 0
        print(f"\n[Etapa 4] Alterando o bit {bit_alvo} para 0...")

        if not cliente.escrever_bit_individual(endereco_comando, bit_alvo, 0):
            print("Falha ao desativar o bit.")
            cliente.fechar()
            return

        bits_apos_0 = cliente.ler_bits_registrador(endereco_comando)
        print(f"Novo estado: {bits_apos_0}")

        # 5. Verificação da preservação dos outros bits
        if bits_apos_1 is not None and bits_apos_0 is not None:
            preservados = all(
                bits_iniciais[i] == bits_apos_1[i] == bits_apos_0[i]
                for i in range(16) if i != bit_alvo
            )
            print(f"\nOutros bits preservados: {preservados}")

        print("\nDemonstração concluída!")

        cliente.fechar()
    else:
        print("Falha ao conectar no servidor. Verifique se ele está em execução.")

if __name__ == '__main__':
    executar_demonstracao_bits()