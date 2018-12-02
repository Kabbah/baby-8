# -*- coding: utf-8 -*-
# ==============================================================================
# audio.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-22
# ==============================================================================

import os
import random
import threading
import time

# ==============================================================================

# Diretório de audio
AUDIO_DIR = "/home/pi/oficina/voice"

AUDIO_FILES = ["voice01.mp3", "voice02.mp3", "voice03.mp3", "voice04.mp3",
               "voice05.mp3", "voice06.mp3", "voice07.mp3", "voice08.mp3",
               "voice09.mp3", "voice10.mp3", "voice11.mp3", "voice12.mp3",
               "voice13.mp3", "voice14.mp3", "voice15.mp3", "voice16.mp3"]

MIN_TIME = 8.0
MAX_TIME = 15.0

# ==============================================================================

class Audio(threading.Thread):
    """
    Thread que faz o controle do áudio do robô.
    """
    
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
    
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
        Periodicamente coloca um som pra tocar. Sorteia um som da lista
        AUDIO_FILES e sorteia também o tempo para tocar o próximo som entre
        MAX_TIME e MIN_TIME.
        """
        begin_time = 0.0
        end_time = 0.0
        
        while not self.stopped():
            if time.time() > end_time:
                begin_time = time.time()
                
                # Seleciona um arquivo de som aleatório
                audio_file = AUDIO_DIR + "/" + random.choice(AUDIO_FILES)
                
                os.system("omxplayer " + audio_file)
                
                # Espera um tempo aleatório (8 - 15 segundos)
                random_time = MIN_TIME + random.random() * (MAX_TIME - MIN_TIME)
                end_time = begin_time + random_time
            time.sleep(0.5)
    
    # --------------------------------------------------------------------------
    
# ==============================================================================
