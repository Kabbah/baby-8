# -*- coding: utf-8 -*-
# ==============================================================================
# servo_motor.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-22
# ==============================================================================

import RPi.GPIO as GPIO

# ==============================================================================

# Valor usual de frequência para PWM de servomotor
SERVO_PWM_FREQ = 50.0 # Hz

# ==============================================================================

class ServoMotor(object):
    """
    Classe que implementa funções para controlar um servomotor.
    """
    
    def __init__(self, pin):
        """
        Inicializa o servomotor com o pino especificado, aplicando um duty cycle
        de 0%.
        Supõe que a função `RPi.GPIO.setmode()` já foi chamada.
        
        :param pin: número do pino de controle do servomotor
        :type pin: int
        """
        self.pin = pin
        self.duty_cycle = 0.0
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, SERVO_PWM_FREQ)
        self.pwm.start(self.duty_cycle)
    
    # --------------------------------------------------------------------------
    
    def set_duty_cycle(self, duty_cycle):
        """
        Altera o duty cycle do servo motor para o valor especificado.
        
        :param duty_cycle: valor do novo duty cycle (entre 0 e 100)
        :type duty_cycle: float
        """
        self.pwm.ChangeDutyCycle(duty_cycle)
        self.duty_cycle = duty_cycle

# ==============================================================================
