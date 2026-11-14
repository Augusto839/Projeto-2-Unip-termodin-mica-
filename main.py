import time
import json
import socket
import network
from machine import Pin, ADC, I2C
from bmp280 import BMP280

# WIFI
WIFI_NOME = "NOME_DA_REDE"
WIFI_SENHA = "SUA_SENHA_DO_WIFI"

# SERVIDOR FLASK
IP_SERVIDOR = "IP_LOCAL_DO_SERVIDOR"
PORTA = 5000

# BMP280
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
bmp = BMP280(i2c)

# LDR
sensor_luz = Pin(25, Pin.IN)

# MQ-135
sensor_gas = ADC(Pin(35))
sensor_gas.atten(ADC.ATTN_11DB)

def ler_sensores():
    temperatura = None
    pressao = None

    try:
        temperatura, pressao = bmp.ler()
    except Exception as erro:
        print("Erro no BMP280:", erro)

    return {
        "temperatura": temperatura,
        "umidade": None,
        "pressao": pressao,
        "qualidade_ar": sensor_gas.read(),
        "luminosidade": sensor_luz.value(),
        "pluviometria": None
    }

def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    if not wifi.isconnected():
        wifi.connect(WIFI_NOME, WIFI_SENHA)

        while not wifi.isconnected():
            print("Conectando ao Wi-Fi...")
            time.sleep(1)

    print("Wi-Fi conectado!")
    print("IP do ESP32:", wifi.ifconfig()[0])

def enviar_dados(dados):
    corpo = json.dumps(dados)

    requisicao = (
        "POST /dados HTTP/1.1\r\n"
        "Host: " + IP_SERVIDOR + "\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: " + str(len(corpo)) + "\r\n"
        "Connection: close\r\n\r\n"
        + corpo
    )

    endereco = socket.getaddrinfo(IP_SERVIDOR, PORTA)[0][-1]
    s = socket.socket()
    s.settimeout(10)

    try:
        s.connect(endereco)
        s.send(requisicao.encode())
        resposta = s.recv(512)
    finally:
        s.close()

    return resposta.split(b"\r\n")[0].decode()

conectar_wifi()

while True:
    try:
        dados = ler_sensores()

        print("--------------------")
        print("Temperatura:", dados["temperatura"])
        print("Pressao:", dados["pressao"])
        print("Qualidade do ar:", dados["qualidade_ar"])
        print("Luminosidade:", dados["luminosidade"])

        status = enviar_dados(dados)
        print("Resposta do Flask:", status)

    except Exception as erro:
        print("Erro:", erro)

    time.sleep(10)
