from pymodbus.client import ModbusTcpClient


class ClienteMODBUS():
    """
    Classe Cliente MODBUS usando pymodbus
    """
    def __init__(self, server_ip, porta, scan_time=1):
        """
        Construtor
        """
        # Cria o cliente TCP
        self._cliente = ModbusTcpClient(host=server_ip, port=porta)
        self._scan_time = scan_time

    def conectar(self):
        """Abre a conexão com o servidor"""
        return self._cliente.connect()

    def fechar(self):
        """Fecha a conexão com o servidor"""
        self._cliente.close()

    def lerDado(self, tipo, addr):
        """
        Método para leitura de um dado da Tabela MODBUS
        Retorna o valor lido ou None em caso de falha.
        """
        # Holding Register (função 03)
        if tipo == 1:
            resp = self._cliente.read_holding_registers(address=addr, count=1, device_id=1)
            if resp and not resp.isError():
                return resp.registers[0]
            return None

        # Coil (função 01)
        if tipo == 2:
            resp = self._cliente.read_coils(address=addr, count=1, device_id=1)
            if resp and not resp.isError():
                return resp.bits[0]
            return None

        # Input Register (função 04)
        if tipo == 3:
            resp = self._cliente.read_input_registers(address=addr, count=1, device_id=1)
            if resp and not resp.isError():
                return resp.registers[0]
            return None

        # Discrete Input (função 02)
        if tipo == 4:
            resp = self._cliente.read_discrete_inputs(address=addr, count=1, device_id=1)
            if resp and not resp.isError():
                return resp.bits[0]
            return None

        # Tipo inválido
        return None

    def escreveDado(self, tipo, addr, valor):
        """
        Método para a escrita de dados na Tabela MODBUS
        Retorna True em caso de sucesso, False em caso de falha.
        """
        # Holding Register (função 06 - single)
        if tipo == 1:
            resp = self._cliente.write_register(address=addr, value=valor, device_id=1)
            return bool(resp and not resp.isError())

        # Coil (função 05 - single)
        if tipo == 2:
            # Em coils, valor esperado é 0/1 (False/True)
            resp = self._cliente.write_coil(address=addr, value=bool(valor), device_id=1)
            return bool(resp and not resp.isError())

        # Tipo inválido
        return False

    #Implementações de métodos para a atividade 2
    def ler_float(self, addr):
        """
        Lê dois Holding Registers consecutivos e converte para float32.
        """
        # Lê 2 registradores a partir do endereço
        resp = self._cliente.read_holding_registers(address=addr, count=2, device_id=1)

        if resp and not resp.isError():
            # Decodifica os dois registradores para float32
            # Mesma ordem de palavras utilizada no servidor
            valor_float = ModbusTcpClient.convert_from_registers(
                resp.registers,
                data_type=ModbusTcpClient.DATATYPE.FLOAT32,
                word_order="little"
            )
            return valor_float
        return None

    def escrever_float(self, addr, valor):
        """
        Converte um float32 em dois registradores e os escreve no servidor.
        """
        payload = ModbusTcpClient.convert_to_registers(
            valor,
            data_type=ModbusTcpClient.DATATYPE.FLOAT32,
            word_order="little"
        )

        # Escreve os 2 registradores gerados
        resp = self._cliente.write_registers(address=addr, values=payload, device_id=1)

        return bool(resp and not resp.isError())

    def ler_bits_registrador(self, addr):
        """
        Lê um registrador e retorna uma lista com o estado dos seus 16 bits (0 ou 1).
        O bit 0 é o menos significativo (posição 0 da lista).
        """
        resp = self._cliente.read_holding_registers(address=addr, count=1, device_id=1)

        if resp and not resp.isError():
            valor = resp.registers[0]
            # Cria uma lista verificando cada bit de 0 a 15
            bits = [(valor >> i) & 1 for i in range(16)]
            return bits
        return None

    def escrever_bit_individual(self, addr, bit_index, valor_bit):
        """
        Altera um bit específico (0-15) de um registrador, preservando os demais.
        valor_bit deve ser 0 ou 1.
        """
        if not (0 <= bit_index <= 15):
            print("Índice de bit inválido.")
            return False

        if valor_bit not in (0, 1):
            print("Valor do bit inválido. Utilize 0 ou 1.")
            return False

        # 1. Lê o registrador atual
        resp_leitura = self._cliente.read_holding_registers(address=addr, count=1, device_id=1)

        if not resp_leitura or resp_leitura.isError():
            return False
            
        valor_atual = resp_leitura.registers[0]
        
        # 2. Aplica a máscara para alterar o bit
        if valor_bit == 1:
            # Força o bit para 1 usando OR (|)
            novo_valor = valor_atual | (1 << bit_index)
        else:
            # Força o bit para 0 usando AND (&) com o inverso (~) da posição
            novo_valor = valor_atual & ~(1 << bit_index)
            
        # 3. Escreve o valor modificado de volta
        resp_escrita = self._cliente.write_register(
            address=addr, value=novo_valor, device_id=1
        )

        return bool(resp_escrita and not resp_escrita.isError())