import sys
import os
from time import sleep

# Adiciona o diretório raiz ao path para conseguir importar a pasta cliente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cliente.clientemodbus import ClienteMODBUS

def executar_demonstracao_float_e_escala():
    # Inicializa o cliente (ajuste o IP e porta conforme o seu servidor)
    cliente = ClienteMODBUS('127.0.0.1', 502)
    
    if cliente.conectar():
        print("Conectado ao servidor MODBUS com sucesso!\n")
        
        # --- DEMONSTRAÇÃO 1: Escala em número inteiro ---
        # Utilizando V_pv1 (Endereço 700, Div = 10, Multiplicador = 0,1)
        endereco_tensao = 700
        div = 10
        multiplicador = 0.1
        
        print("[Demonstração de Escala]")
        # Vamos simular que o servidor tem o valor 2450 (que representa 245.0 V)
        # Escrevemos o valor numérico bruto apenas para o teste do cliente
        cliente.escreveDado(1, endereco_tensao, 2450)
        sleep(1)
        
        valor_numerico = cliente.lerDado(1, endereco_tensao)
        if valor_numerico is not None:
            valor_engenharia = valor_numerico * multiplicador
            print(f"Dado lido: V_pv1 (Endereço {endereco_tensao})")
            print(f"Valor numérico recebido: {valor_numerico}")
            print(f"Div: {div} | Multiplicador: {multiplicador}")
            print(f"Valor de engenharia calculado: {valor_engenharia:.1f} V\n")
            
        # --- DEMONSTRAÇÃO 2: Escrita e Leitura de Float32 (FP) ---
        # Utilizando Bat_charge_power (Endereço 1204-1205, FP, Div = 1)
        endereco_fp = 1204
        valor_enviado_fp = 3540.75
        
        print("[Demonstração de Float32]")
        print(f"A escrever {valor_enviado_fp} em Bat_charge_power (Endereços {endereco_fp}-{endereco_fp+1})...")
        sucesso_escrita = cliente.escrever_float(endereco_fp, valor_enviado_fp)
        sleep(1)
        
        if sucesso_escrita:
            valor_lido_fp = cliente.ler_float(endereco_fp)
            print(f"Valor lido do servidor: {valor_lido_fp}")
            # A comparação exata de floats pode ter pequenas variações de precisão
            print(f"Diferença da precisão: {abs(valor_enviado_fp - valor_lido_fp):.6f}")
        else:
            print("Falha ao escrever o valor Float32.")
            
        cliente.fechar()
    else:
        print("Falha ao conectar no servidor. Verifique se ele está em execução.")

if __name__ == '__main__':
    executar_demonstracao_float_e_escala()