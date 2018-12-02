# -*- coding: utf-8 -*-
# ==============================================================================
# cabeca.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-22
# ==============================================================================

import threading
import time

from servo_motor import ServoMotor

# ==============================================================================

# Pino de controle do servomotor contínuo
SERVO_PINO_CTRL = 12 # GPIO.BOARD

# Valor de duty cycle em que o motor fica aproximadamente parado
SERVO_DUTY_CYCLE_MEIO = 7.25 # %

# Offset a partir do valor anterior para as velocidades máximas
SERVO_MAX_VELOC_OFFSET = 3.25 # %

# Tempo entre atualizações de velocidade (0 < tempo < 1).
# O incremento de velocidade é computado para chegar na velocidade máxima em um
# segundo.
TEMPO_ATU_VEL = 0.1 # s

# ==============================================================================

class Cabeca(threading.Thread):
    """
    Thread que faz o controle da cabeça do robô. Verifica se deve movimentar o
    servomotor e implementa uma rampa de aceleração e desaceleração.
    """
    
    def __init__(self, robo):
        """
        Instancia o servomotor contínuo.
        Supõe que a função `RPi.GPIO.setmode()` já foi chamada.
        """
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        
        self.robo = robo
        self.servo = ServoMotor(SERVO_PINO_CTRL)
        
        self.velocidade = SERVO_DUTY_CYCLE_MEIO
        self.veloc_max_horario = SERVO_DUTY_CYCLE_MEIO - SERVO_MAX_VELOC_OFFSET
        self.veloc_max_antihor = SERVO_DUTY_CYCLE_MEIO + SERVO_MAX_VELOC_OFFSET
        
        self.incremento_veloc = SERVO_MAX_VELOC_OFFSET * TEMPO_ATU_VEL
    
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
        Verifica periodicamente se há um comando para movimentar o servomotor.
        Se houver, altera a velocidade do motor segundo uma rampa linear.
        Caso não haja comando algum e o motor estiver se movendo, freia o motor
        segundo uma rampa linear até sua parada completa.
        """
        while not self.stopped():
            # Lê o comando mais novo
            servo_cmd = self.robo.servo
        
            # Verifica se o comando de girar servo no sentido horário está ativo
            if servo_cmd < 0.0:
                self.__update_speed_cw()
            
            # Verifica se o comando de girar servo no sentido antihorário está ativo
            elif servo_cmd > 0.0:
                self.__update_speed_countercw()
            
            # Para o servomotor lentamente
            else:
                self.__update_speed_stop()
            
            # Espera
            time.sleep(TEMPO_ATU_VEL)
    
    # --------------------------------------------------------------------------
    
    def __update_speed_cw(self):
        """
        Incrementa a velocidade do servomotor para o sentido horário.
        """
        if self.velocidade > self.veloc_max_horario:
            self.velocidade -= self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade < self.veloc_max_horario:
                self.velocidade = self.veloc_max_horario
            
            self.servo.set_duty_cycle(self.velocidade)
    
    # --------------------------------------------------------------------------

    def __update_speed_countercw(self):
        """
        Incrementa a velocidade do servomotor para o sentido antihorário.
        """
        if self.velocidade < self.veloc_max_antihor:
            self.velocidade += self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade > self.veloc_max_antihor:
                self.velocidade = self.veloc_max_antihor
            
            self.servo.set_duty_cycle(self.velocidade)
    
    # --------------------------------------------------------------------------
    
    def __update_speed_stop(self):
        """
        Para o servomotor lentamente.
        """
        if self.velocidade > SERVO_DUTY_CYCLE_MEIO:
            self.velocidade -= self.incremento_veloc
            
            # Para mesmo que haja arredondamento de float
            if self.velocidade <= SERVO_DUTY_CYCLE_MEIO:
                self.velocidade = SERVO_DUTY_CYCLE_MEIO
                self.servo.set_duty_cycle(0.0)
            else:
                self.servo.set_duty_cycle(self.velocidade)
        elif self.velocidade < SERVO_DUTY_CYCLE_MEIO:
            self.velocidade += self.incremento_veloc
            
            # Para mesmo que haja arredondamento de float
            if self.velocidade >= SERVO_DUTY_CYCLE_MEIO:
                self.velocidade = SERVO_DUTY_CYCLE_MEIO
                self.servo.set_duty_cycle(0.0)
            else:
                self.servo.set_duty_cycle(self.velocidade)
        else:
            self.servo.set_duty_cycle(0.0)
    
# ==============================================================================
