# -*- coding: utf-8 -*-
# ==============================================================================
# motor_dc.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-22
# ==============================================================================

import RPi.GPIO as GPIO

# ==============================================================================

# Valor usual de frequência para PWM de motor DC
MOTOR_PWM_FREQ = 50.0 # Hz

# ==============================================================================

class MotorDC(object):
    """
    Classe que implementa funções para controlar um motor DC com controle de
    velocidade por PWM.
    """
    
    def __init__(self, pin_a, pin_b):
        """
        Inicializa o motor com os pinos especificado, aplicando um duty cycle
        de 0%.
        Supõe que a função `RPi.GPIO.setmode()` já foi chamada.
        
        :param pin_a: número do pino A de controle do motor DC
        :type pin_a: int
        :param pin_b: número do pino A de controle do motor DC
        :type pin_b: int
        """
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.duty_cycle = 0.0
        GPIO.setup(self.pin_a, GPIO.OUT)
        GPIO.setup(self.pin_b, GPIO.OUT)
        self.pwm_a = GPIO.PWM(self.pin_a, MOTOR_PWM_FREQ)
        self.pwm_b = GPIO.PWM(self.pin_b, MOTOR_PWM_FREQ)
        self.pwm_a.start(self.duty_cycle)
        self.pwm_b.start(self.duty_cycle)
    
    # --------------------------------------------------------------------------
    
    def set_duty_cycle(self, duty_cycle, forward):
        """
        Altera o duty cycle do motor para o valor especificado, na direção
        especificada.
        
        :param duty_cycle: valor do novo duty cycle (entre 0 e 100)
        :type duty_cycle: float
        :param forward: indica se o sentido é para a frente
        :type forward: boolean
        """
        if forward:
            self.pwm_b.ChangeDutyCycle(0.0)
            self.pwm_a.ChangeDutyCycle(duty_cycle)
        else:
            self.pwm_a.ChangeDutyCycle(0.0)
            self.pwm_b.ChangeDutyCycle(duty_cycle)
        self.duty_cycle = duty_cycle

# ==============================================================================
