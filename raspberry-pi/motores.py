# -*- coding: utf-8 -*-
# ==============================================================================
# motores.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-22
# ==============================================================================

import threading
import time

from motor_dc import MotorDC

# ==============================================================================

# Pinos de controle do motor esquerdo
MOTOR_ESQ_PINO_A = 16 # GPIO.BOARD
MOTOR_ESQ_PINO_B = 15 # GPIO.BOARD

# Pinos de controle do motor direito
MOTOR_DIR_PINO_A = 36 # GPIO.BOARD
MOTOR_DIR_PINO_B = 38 # GPIO.BOARD

# Tempo entre atualizações de velocidade (0 < tempo < 1).
# O incremento de velocidade é computado para chegar na velocidade máxima em um
# segundo.
TEMPO_ATU_VEL = 0.1 # s

# Distância a partir da qual o robô para
DIST_US_PARAR = 100.0 # cm

# ==============================================================================

class Motores(threading.Thread):
    """
    Thread que faz o controle dos motores DC do robô. Verifica se deve
    movimentar o robô para frente, trás ou rotação, aciona os motores
    necessários e implementa uma rampa de aceleração e desaceleração.
    """
    
    def __init__(self, robo):
        """
        Instancia os motores DC.
        Supõe que a função `RPi.GPIO.setmode()` já foi chamada.
        """
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        
        self.robo = robo
        self.motor_esq = MotorDC(MOTOR_ESQ_PINO_A, MOTOR_ESQ_PINO_B)
        self.motor_dir = MotorDC(MOTOR_DIR_PINO_A, MOTOR_DIR_PINO_B)
        
        self.velocidade_esq = 0.0
        self.velocidade_dir = 0.0
        
        self.incremento_veloc = 100.0 * TEMPO_ATU_VEL
    
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
        Verifica periodicamente se há um comando para movimentar os motores.
        Se houver, altera a velocidade dos motores segundo uma rampa linear.
        Caso não haja comando algum e os motores estiverem se movendo, freia os
        motores segundo uma rampa linear até sua parada completa.
        """
        while not self.stopped():
            motor_vel_cmd = self.robo.motor_vel
            motor_rot_cmd = self.robo.motor_rot
            
            if motor_vel_cmd != 0 and motor_rot_cmd != 0:
                # MUITO IMPROVÁVEL: ocorreu um comando entre as leituras dessa
                # thread. Vai para a próxima iteração.
                # (não quis colocar uma Lock para não prejudicar o desempenho)
                continue
            
            
            # Verifica se deve movimentar os motores para a frente
            if motor_vel_cmd > 0:
                # Verifica distância do ultrassônico
                if self.robo.leitor_distancia.sensor > DIST_US_PARAR:
                    self.__update_speed_forward()
            # Verifica se deve movimentar os motores para trás
            elif motor_vel_cmd < 0:
                # Verifica distância do ultrassônico
                if self.robo.leitor_distancia.sensor > DIST_US_PARAR:
                    self.__update_speed_backward()
            # Verifica se deve rotacionar os motores em sentido horário
            elif motor_rot_cmd < 0:
                self.__update_speed_rotate_cw()
            # Verifica se deve rotacionar os motores em sentido antihorário
            elif motor_rot_cmd > 0:
                self.__update_speed_rotate_counter_cw()
            # Caso base: para gradualmente
            else:
                self.__update_speed_stop()
            
            # Espera
            time.sleep(TEMPO_ATU_VEL)
    
    # --------------------------------------------------------------------------
    
    def __update_speed_forward(self):
        self.__increment_speed_left()
        self.__increment_speed_right()
        
        self.__commit_speed()

    # --------------------------------------------------------------------------
    
    def __update_speed_backward(self):
        self.__decrement_speed_left()
        self.__decrement_speed_right()
        
        self.__commit_speed()
    
    # --------------------------------------------------------------------------
    
    def __update_speed_rotate_cw(self):
        self.__increment_speed_left()
        self.__decrement_speed_right()
        
        self.__commit_speed()

    # --------------------------------------------------------------------------
    
    def __update_speed_rotate_counter_cw(self):
        self.__decrement_speed_left()
        self.__increment_speed_right()
        
        self.__commit_speed()
    
    # --------------------------------------------------------------------------
    
    def __update_speed_stop(self):
        if self.velocidade_esq < 0:
            self.velocidade_esq += self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade_esq > 0:
                self.velocidade_esq = 0
        elif self.velocidade_esq > 0:
            self.velocidade_esq -= self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade_esq < 0:
                self.velocidade_esq = 0
        
        if self.velocidade_dir < 0:
            self.velocidade_dir += self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade_dir > 0:
                self.velocidade_dir = 0
        elif self.velocidade_dir > 0:
            self.velocidade_dir -= self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade_dir < 0:
                self.velocidade_dir = 0
        
        self.__commit_speed()
    
    # --------------------------------------------------------------------------
    
    def __increment_speed_left(self):
        if self.velocidade_esq < 100.0:
            self.velocidade_esq += self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade_esq > 100.0:
                self.velocidade_esq = 100.0

    # --------------------------------------------------------------------------
    
    def __increment_speed_right(self):
        if self.velocidade_dir < 100.0:
            self.velocidade_dir += self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade_dir > 100.0:
                self.velocidade_dir = 100.0

    # --------------------------------------------------------------------------
    
    def __decrement_speed_left(self):
        if self.velocidade_esq > -100.0:
            self.velocidade_esq -= self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade_esq < -100.0:
                self.velocidade_esq = -100.0

    # --------------------------------------------------------------------------
    
    def __decrement_speed_right(self):
        if self.velocidade_dir > -100.0:
            self.velocidade_dir -= self.incremento_veloc
            
            # Corrige float caso necessário
            if self.velocidade_dir < -100.0:
                self.velocidade_dir = -100.0

    # --------------------------------------------------------------------------
    
    def __commit_speed(self):
        if self.velocidade_esq < 0:
            self.motor_esq.set_duty_cycle(-self.velocidade_esq, False)
        else:
            self.motor_esq.set_duty_cycle(self.velocidade_esq, True)
        
        if self.velocidade_dir < 0:
            self.motor_dir.set_duty_cycle(-self.velocidade_dir, False)
        else:
            self.motor_dir.set_duty_cycle(self.velocidade_dir, True)

# ==============================================================================
