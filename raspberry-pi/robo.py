# -*- coding: utf-8 -*-
# ==============================================================================
# robo.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-24
# ==============================================================================

import RPi.GPIO as GPIO

from audio import Audio
from cabeca import Cabeca
from celular import Celular
from leitor_distancia import LeitorDistancia
from motores import Motores

# ==============================================================================



# ==============================================================================

class Robo(object):
    """
    Classe que une todas as partes do robô.
    """
    
    def __init__(self):
        """
        """
        GPIO.setmode(GPIO.BOARD)
        
        self.cabeca = Cabeca(self)
        self.motores = Motores(self)
        self.leitor_distancia = LeitorDistancia()
        self.celular = Celular()
        self.audio = Audio()
        
        self.servo = 0.0
        self.motor_vel = 0.0
        self.motor_rot = 0.0
    
    # --------------------------------------------------------------------------
    
    def run(self):
        """
        """
        self.cabeca.start()
        self.motores.start()
        self.leitor_distancia.start()
        self.audio.start()
        
        try:
            while True:
                self.celular.wait_phone()
                
                try:
                    while True:
                        cmd = self.celular.get_next_command()
                        if cmd is None:
                            continue
                        
                        if cmd[0] == "head":
                            self.servo = cmd[1]
                        elif cmd[0] == "body":
                            self.motor_vel = cmd[1]
                            self.motor_rot = cmd[2]
                except IOError:
                    self.servo = 0.0
                    self.motor_vel = 0.0
                    self.motor_rot = 0.0
        finally:
            # Finalizar todas as threads e sair
            self.cabeca.stop()
            self.motores.stop()
            self.leitor_distancia.stop()
            self.cabeca.join()
            self.motores.join()
            self.leitor_distancia.join()
            GPIO.cleanup()
    
    # --------------------------------------------------------------------------
    
    def stop_threads(self):
        self.cabeca.stop()
        self.motores.stop()
        self.leitor_distancia.stop()
        self.audio.stop()
    
    # --------------------------------------------------------------------------
    
    def join_threads(self, timeout):
        if timeout is None:
            self.cabeca.join()
            self.motores.join()
            self.leitor_distancia.join()
            self.audio.join()
        else:
            self.cabeca.join(timeout)
            self.motores.join(timeout)
            self.leitor_distancia.join(timeout)
            self.audio.join(timeout)

# ==============================================================================
