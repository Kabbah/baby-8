# -*- coding: utf-8 -*-
# ==============================================================================
# celular.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-23
# ==============================================================================

import re

from bluetooth_conn import BluetoothConn

# ==============================================================================

UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

# ==============================================================================

class Celular(object):
    """
    Classe que faz a comunicação com a estação base (celular) por meio de
    Bluetooth.
    Não foi implementada como uma thread porque é executada na thread main.
    """
    
    def __init__(self):
        """
        """
        self.bt = BluetoothConn()
        self.bt.bind_listen_advertise("SampleServer", UUID)
    
    # --------------------------------------------------------------------------
    
    @staticmethod
    def bt_data_protocol(data):
        """
        Processa um comando enviado do celular para o robô.
        
        :param data: dados do comando
        :type data: str
        """
        data = data.replace(",", ".")

        pattern_number = "[-]?[0-9]+([,|.][0-9]+)?"
        pattern_head_cmd = "head " + pattern_number
        pattern_body_cmd = "body " + pattern_number + " " + pattern_number
        
        match_obj = re.search(pattern_body_cmd, data)
        if match_obj is not None and data == match_obj.group(0):
            cmd, v1, v2 = data.split(" ")
            return [cmd, float(v1), float(v2)]
        
        match_obj = re.search(pattern_head_cmd, data)
        if match_obj is not None and data == match_obj.group(0):
            cmd, v1 = data.split(" ")
            return [cmd, float(v1)]
        return None
    
    # --------------------------------------------------------------------------
    
    def wait_phone(self):
        """
        """
        self.bt.accept()
    
    # --------------------------------------------------------------------------
    
    def get_next_command(self):
        """
        Aguarda o comando do celular, faz parse e retorna.
        
        Um comando de movimentação do corpo é dado por uma lista de três itens,
        em que o primeiro item é uma string igual a "body", o segundo item é um
        número que indica movimento para a frente (+), trás (-) ou parado (0), e
        o terceiro item é um número que indica rotação no sentido antihorário
        (+), horário (-) ou sem rotação (0).
        Exemplo: ["body", 0.75, 0.00]
        
        Um comando de movimentação da cabeça é dado por uma lista de dois itens,
        em que o primeiro item é uma string igual a "head" e o segundo item é um
        número que indica rotação no sentido antihorário (+), horário (-) ou sem
        rotação (0).
        Exemplo: ["head", -0.75]
        
        Caso o comando seja inválido, retorna None.
        
        Caso a conexão com o celular seja interrompida, lança uma exceção
        IOError.
        
        :return: lista com o nome do comando e valor(es)
        :rtype: list
        """
        return Celular.bt_data_protocol(self.bt.recv(1024))

# ==============================================================================
