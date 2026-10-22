from pyModbusTCP.server import DataBank, ModbusServer
import random
from time import sleep
from pymodbus.client import ModbusTcpClient


class ServidorMODBUS():
    """
    Classe Servidor Modbus
    """

    def __init__(self, host_ip, port):
        """
        Construtor
        """
        self._db = DataBank()
        self._server = ModbusServer(
            host=host_ip, port=port, no_block=True, data_bank=self._db)

    def inicializar_registradores(self):
        # Inicializa registradores e coils

        # Tensão das Entradas PV
        self._db.set_input_registers(700, [7500])
        self._db.set_input_registers(701, [7500])

        # Corrente das Entradas PV
        self._db.set_input_registers(702, [30])
        self._db.set_input_registers(703, [30])

        # Tensão, Corrente e Potência da rede
        self._db.set_input_registers(800, [2200])
        self._db.set_input_registers(801, [150])
        self._db.set_input_registers(900, [3300])

        # Temperatura do Inversor
        self._db.set_input_registers(1000, [500])

        # Potência Máxima de Carregamento e Descarregamento da Bateria
        lista = ModbusTcpClient.convert_to_registers(
            3000.0, data_type=ModbusTcpClient.DATATYPE.FLOAT32,  word_order="little")
        self._db.set_holding_registers(1200, lista)  # float 1

        lista = ModbusTcpClient.convert_to_registers(
            2800.5, data_type=ModbusTcpClient.DATATYPE.FLOAT32,  word_order="little")
        self._db.set_holding_registers(1202, lista)  # float 2

        # Potência de Carregamento e Descarregamento da Bateria
        lista = ModbusTcpClient.convert_to_registers(
            0.0, data_type=ModbusTcpClient.DATATYPE.FLOAT32,  word_order="little")
        self._db.set_holding_registers(1204, lista)

        lista = ModbusTcpClient.convert_to_registers(
            0.0, data_type=ModbusTcpClient.DATATYPE.FLOAT32,  word_order="little")
        self._db.set_holding_registers(1206, lista)

        # Habilita/Desabilita a Bateria
        self._db.set_coils(1300, [True])

    def atualizar_medicoes(self):
        # Atualiza as grandezas simuladas

        # Tensão das Entradas PV
        self._db.set_input_registers(
            700, [random.randrange(int(0.5*7500), int(1.05*7500))])
        self._db.set_input_registers(
            701, [random.randrange(int(0.5*7500), int(1.05*7500))])

        # Corrente das Entradas PV
        self._db.set_input_registers(
            702, [random.randrange(int(0.5*30), int(1.5*30))])
        self._db.set_input_registers(
            703, [random.randrange(int(0.5*30), int(1.5*30))])

        # Tensão, Corrente e Potência da rede
        self._db.set_input_registers(
            800, [random.randrange(int(0.995*2200), int(1.005*2200))])
        self._db.set_input_registers(
            801, [random.randrange(int(0.5*150), int(1.5*150))])
        self._db.set_input_registers(
            int(900), [random.randrange(int(0.5*3300), int(1.5*3300))])

        # Temperatura do Inversor
        self._db.set_input_registers(
            1000, [random.randrange(int(0.5*500), int(1.5*500))])

        # Potência de Carregamento e Descarregamento da Bateria
        coil_1300 = self._db.get_coils(1300)[0]
        val_to_reg1 = random.uniform(0.0, 3000.0) if coil_1300 == 1 else 0.0
        val_to_reg2 = random.uniform(0.0, 3000.0) if coil_1300 == 1 else 0.0
        self._db.set_holding_registers(1204, ModbusTcpClient.convert_to_registers(
            val_to_reg1, data_type=ModbusTcpClient.DATATYPE.FLOAT32,  word_order="little"))
        self._db.set_holding_registers(1206, ModbusTcpClient.convert_to_registers(
            val_to_reg2, data_type=ModbusTcpClient.DATATYPE.FLOAT32,  word_order="little"))

    def ler_comandos(self):
        # Obtém setpoint e estado de Battery_Enable
        self._db.get_coils(1300)

    def run(self):
        """
        Execução do servidor Modbus
        """
        try:
            self._server.start()
            print("Servidor MODBUS em execução")
            self.inicializar_registradores()
            while True:
                self.atualizar_medicoes()
                sleep(1)
                print("Registradores atualizados")
                print(
                      ModbusTcpClient.convert_from_registers(self._db.get_holding_registers(1200, 2),
                                                             data_type=ModbusTcpClient.DATATYPE.FLOAT32,
                                                             word_order="little"))
                print(
                      ModbusTcpClient.convert_from_registers(self._db.get_holding_registers(1202, 2),
                                                             data_type=ModbusTcpClient.DATATYPE.FLOAT32,
                                                             word_order="little"))
                

        except Exception as e:
            print("Erro: ", e.args)


if __name__ == "__main__":

    s = ServidorMODBUS("localhost", 502)
    s.run()
