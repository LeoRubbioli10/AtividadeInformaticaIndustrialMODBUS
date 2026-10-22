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
        self._db.set_holding_registers(700, [7500])
        self._db.set_holding_registers(701, [7500])

        # Corrente das Entradas PV
        self._db.set_holding_registers(702, [30])
        self._db.set_holding_registers(703, [30])

        # Tensão, Corrente e Potência da rede
        self._db.set_holding_registers(800, [2200])
        self._db.set_holding_registers(801, [150])
        self._db.set_holding_registers(900, [3300])

        # Temperatura do Inversor
        self._db.set_holding_registers(1000, [500])

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

        # Habilita/Desabilita o Carregamento da Bateria
        self._db.set_holding_registers(1300, [1])

        # Setpoint de Potência de Carregamento da Bateria
        lista = ModbusTcpClient.convert_to_registers(1500.0, data_type=ModbusTcpClient.DATATYPE.FLOAT32, word_order="little")
        self._db.set_holding_registers(1302, lista)

    def atualizar_medicoes(self):
        # Atualiza as grandezas simuladas

        # Tensão das Entradas PV
        self._db.set_holding_registers(
            700, [random.randrange(int(0.98*7500), int(1.02*7500))])
        self._db.set_holding_registers(
            701, [random.randrange(int(0.98*7500), int(1.02*7500))])

        # Corrente das Entradas PV
        self._db.set_holding_registers(
            702, [random.randrange(int(0.9*30), int(1.1*30))])
        self._db.set_holding_registers(
            703, [random.randrange(int(0.9*30), int(1.1*30))])

        # Tensão, Corrente e Potência da rede
        self._db.set_holding_registers(
            800, [random.randrange(int(0.995*2200), int(1.005*2200))])
        self._db.set_holding_registers(
            801, [random.randrange(int(0.9*150), int(1.1*150))])
        self._db.set_holding_registers(
            900, [random.randrange(int(0.9*3300), int(1.1*3300))])

        # Temperatura do Inversor
        self._db.set_holding_registers(
            1000, [random.randrange(int(0.98*500), int(1.02*500))])

        # Potência de Carregamento e Descarregamento da Bateria
        battery_enable, setpoint = self.ler_comandos()

        # Limita o setpoint à potência máxima de carregamento
        setpoint = max(0.0, min(setpoint, 3000.0))

        val_to_reg1 = setpoint if battery_enable == 1 else 0.0
        val_to_reg2 = 0.0

        self._db.set_holding_registers(
            1204, ModbusTcpClient.convert_to_registers(val_to_reg1, data_type=ModbusTcpClient.DATATYPE.FLOAT32, word_order="little"))
        self._db.set_holding_registers(
            1206, ModbusTcpClient.convert_to_registers(val_to_reg2, data_type=ModbusTcpClient.DATATYPE.FLOAT32, word_order="little"))

    def ler_comandos(self):
        # Obtém setpoint e estado de Battery_Enable
        registrador = self._db.get_holding_registers(1300)[0]
        battery_enable = registrador & 1

        lista = self._db.get_holding_registers(1302, 2)
        setpoint = ModbusTcpClient.convert_from_registers(lista, data_type=ModbusTcpClient.DATATYPE.FLOAT32, word_order="little")

        return battery_enable, setpoint

    def run(self):
        """
        Execução do servidor Modbus
        """
        try:
            self.inicializar_registradores()
            self._server.start()
            print("Servidor MODBUS em execução")

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
