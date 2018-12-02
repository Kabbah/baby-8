# -*- coding: utf-8 -*-
# ==============================================================================
# leitor_distancia.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-23
# ==============================================================================

import threading
import time

from bluetooth_conn import BluetoothConn

# ==============================================================================

# Porta a utilizar para se conectar ao Arduino
RASPBERRY_PI_BT_PORT = 1

# Endereço físico do módulo Bluetooth do Arduino
ARDUINO_ADDR = "98:D3:32:30:72:AE"

# Tempo entre polls de distância do Arduino
TEMPO_POLLING = 0.5 # s

# ==============================================================================

class LeitorDistancia(threading.Thread):
    """
    Thread que faz a comunicação com o Arduino na cabeça do robô por Bluetooth.
    """
    
    def __init__(self):
        """
        Instancia o socket Bluetooth e uma leitura dummy inicial.
        """
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        
        self.sensor = 11037.0 # Valor dummy
        self.bt = BluetoothConn()
    
    # --------------------------------------------------------------------------
    
    def stop(self):
        """
        Manda a thread parar na próxima iteração.
        """
        self._stop_event.set()
    
    def stopped(self):
        """
        Indica se o evento de parar foi setado.
        :return: True se o evento foi setado.
        :rtype: boolean
        """
        return self._stop_event.is_set()
    
    # --------------------------------------------------------------------------
    
    def run(self):
        """
        Realiza polling para obter as leituras do sensor ultrassônico.
        Caso haja alguma falha de comunicação entre o Raspberry Pi e o Arduino,
        simplesmente finaliza a thread.
        """
        try:
            self.bt.connect(ARDUINO_ADDR, RASPBERRY_PI_BT_PORT)
            
            while not self.stopped():
                time.sleep(TEMPO_POLLING)
                
                self.bt.send("S")
                try:
                    self.sensor = float(self.bt.recv(1024))
                except ValueError:
                    pass
        except IOError:
            pass
        except bluetooth.BluetoothError:
            pass
    
    # --------------------------------------------------------------------------
    
    def get_sensor_value(self):
        """
        Retorna a última leitura do sensor.
        :return: valor mais recente do sensor
        :rtype: float
        """
        return self.sensor

# ==============================================================================
