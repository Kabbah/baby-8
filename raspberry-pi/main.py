# -*- coding: utf-8 -*-
# ==============================================================================
# main.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-24
# ==============================================================================

import RPi.GPIO as GPIO
import signal
import sys

from robo import Robo

# ==============================================================================

def main():
    robo = Robo()
    
    def sigterm_handler(_signo, _stack):
        robo.stop_threads()
        robo.join_threads(3.0)
        GPIO.cleanup()
        sys.exit(0)
    
    # Configura um handler para SIGTERM
    signal.signal(signal.SIGTERM, sigterm_handler)
    
    robo.run()

if __name__ == "__main__":
    main()

# ==============================================================================
