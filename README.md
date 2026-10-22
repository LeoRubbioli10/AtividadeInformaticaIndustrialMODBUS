# AtividadeInformaticaIndustrialMODBUS

## 1. Descrição

Atividade prática da disciplina **Informática Industrial (ENE118)**, da UFJF, desenvolvida em dupla. O projeto utiliza Python e Modbus TCP para simular um CLP lendo dados de um Inversor Híbrido.

O servidor disponibiliza medições em Holding Registers e atualiza seus valores periodicamente. O cliente realiza leituras, conversões e escritas de registradores, incluindo valores float32 e comandos por bit.

## 2. Integrantes e atribuições

- **Lucas de Faria Cristofaro** — tabela Modbus e servidor.
- **Leonardo Nunes Rubbioli Cordeiro** — tabela Modbus e cliente (testes).

## 3. Organização do projeto

- ServidorMODBUS/servidor_modbus.py — servidor Modbus TCP e emulação do CLP.
- ClienteMODBUS/clientemodbus.py — conexão, leitura, escrita e conversão de dados.
- exemplos/exemplo_float.py — demonstração de float32 e escala.
- exemplos/exemplo_bits.py — demonstração de leitura e escrita de bits.
- requirements.txt — bibliotecas e versões utilizadas.
- .gitignore — exclusão do ambiente virtual e de arquivos temporários.

## 4. Funcionamento do protocolo

A comunicação utiliza Holding Registers Modbus (4X). Variáveis inteiras ocupam 1 registrador de 16 bits, variáveis float32 ocupam 2 registradores consecutivos. Os endereços abaixo são utilizados diretamente nas chamadas da API, sem o prefixo 4xxxx.

Para dados com escala:

- **Leitura:** valor de engenharia = valor recebido / Div.
- **Escrita:** valor a enviar = valor de engenharia x Div.
- **Multiplicador:** m = 1 / Div.

Em float32, primeiro se convertem os dois registradores e depois se aplica o fator de escala. 

### Mapa de registradores

| Tag | Descrição | Tipo | Endereço(s) | Qtd. | Bit | Div | m | Unidade |
|---|---|---|---|---:|---|---:|---:|---|
| V_pv1 | Tensão PV 1 | 4X | 700 | 1 | — | 10 | 0,1 | V |
| V_pv2 | Tensão PV 2 | 4X | 701 | 1 | — | 10 | 0,1 | V |
| I_pv1 | Corrente PV 1 | 4X | 702 | 1 | — | 10 | 0,1 | A |
| I_pv2 | Corrente PV 2 | 4X | 703 | 1 | — | 10 | 0,1 | A |
| V_grid | Tensão da rede | 4X | 800 | 1 | — | 10 | 0,1 | V |
| I_grid | Corrente da rede | 4X | 801 | 1 | — | 10 | 0,1 | A |
| P_grid | Potência da rede | 4X | 900 | 1 | — | 1 | 1 | W |
| Temperature | Temperatura do equipamento | 4X | 1000 | 1 | — | 10 | 0,1 | °C |
| Bat_charge_max_power | Potência máxima de carga | FP | 1200–1201 | 2 | — | 1 | 1 | W |
| Bat_disc_max_power | Potência máxima de descarga | FP | 1202–1203 | 2 | — | 1 | 1 | W |
| Bat_charge_power | Potência de carga | FP | 1204–1205 | 2 | — | 1 | 1 | W |
| Bat_disc_power | Potência de descarga | FP | 1206–1207 | 2 | — | 1 | 1 | W |
| Battery_Enable | Habilitar carregamento da bateria | 4X/bit | 1300 | 1 | 0 | 1 | 1 | 0/1 |
| Bat_charge_sp | Setpoint de potência de carga | FP | 1302–1303 | 2 | — | 1 | 1 | W |

O servidor atualiza as medições a cada 1 segundo, com variações aleatórias limitadas. Quando Battery_Enable (bit 0) está ativo, Bat_charge_power assume o setpoint de carga, quando está desativado, a potência de carga é 0.

## 5. Instalação e execução

Na raiz do repositório:

powershell || cmd
python -m venv .venv
.\.venv\Scripts\Activate.ps1 || \venv\Scripts\activate.bat
python -m pip install -r requirements.txt


Comandos de execução, considerando os caminhos indicados na seção 3:

powershell || cmd
python -m ServidorMODBUS.servidor_modbus

# Em outro terminal, com o ambiente virtual ativo:
python -m exemplos.exemplo_float
python -m exemplos.exemplo_bits

## 6. Demonstrações e testes

- **Emulação:** o servidor implementa 12 dados de medição, atualização periódica e controle de carga por setpoint e bit.

- **Escala:** V_pv1 (700), Div = 10 e multiplicador = 0,1. A leitura anterior retornou 0 por usar Input Register (FC04); o exemplo foi corrigido para Holding Register (FC03), mas o resultado após a correção ainda não foi informado.

- **Float32:** escrita e leitura do valor 3540.75 em Bat_charge_max_power (1200–1201), com recuperação correta do valor e diferença de precisão de 0.000000.

- **Bits:** teste concluído no Holding Register **1300**, bit **0**. O valor inicial **42** (bits 1, 3 e 5 ativos) passou para **43** ao ativar o bit 0 e retornou a **42** ao desativá-lo. A verificação indicou **Outros bits preservados: True**.

## 7. Versionamento e entrega

Cada integrante desenvolve em sua própria branch, registra commits e revisa as alterações do colega antes da integração à main. A entrega é feita pelo link do repositório GitHub postado no Google Classroom.