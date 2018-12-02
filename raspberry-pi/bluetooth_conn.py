# -*- coding: utf-8 -*-
# ==============================================================================
# bluetooth_conn.py
#
# Autor: Victor Barpp Gomes
# Data: 2018-10-23
# ==============================================================================

import sys
sys.path.append('/home/pi/.local/lib/python2.7/site-packages')

import bluetooth

# ==============================================================================

class BluetoothConn(object):
    """
    Classe que condensa todas as chamadas de função do PyBluez.
    """
    
    def __init__(self):
        """
        Cria um objeto socket limpo.
        Este socket pode funcionar tanto como servidor, por meio das chamadas
        bind_listen_advertise() e accept(), ou como cliente, por meio da chamada
        connect().
        """
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_socket = None
        self.client_info = None
    
    # --------------------------------------------------------------------------
    
    def connect(self, mac_addr, port):
        """
        Conecta-se ao dispositivo Bluetooth especificado pelo endereço físico.
        
        :param mac_addr: endereço físico a se conectar
        :type mac_addr: str
        :param port: porta Bluetooth
        :type port: int
        """
        self.socket.connect((mac_addr, port))
    
    # --------------------------------------------------------------------------
    
    def bind_listen_advertise(self, name, uuid):
        """
        Faz bind no socket Bluetooth e prepara-o para chamadas accept().
        
        :param port: porta Bluetooth
        :type port: int
        """
        self.socket.bind(("", bluetooth.PORT_ANY))
        self.socket.listen(1)

        # Anuncia o servico
        bluetooth.advertise_service(self.socket, name,
                service_id = uuid,
                service_classes = [uuid, bluetooth.SERIAL_PORT_CLASS],
                profiles = [bluetooth.SERIAL_PORT_PROFILE],
                #protocols = [bluetooth.OBEX_UUID]
        )
    
    # --------------------------------------------------------------------------
    
    def accept(self):
        """
        Aceita uma conexão e armazena os sockets e informações nos atributos da
        classe.
        Bloqueante.
        """
        self.client_socket, self.client_info = self.socket.accept()
    
    # --------------------------------------------------------------------------
    
    def clear_client(self):
        """
        Limpa o socket cliente gerado pelo último accept().
        """
        self.client_socket = None
        self.client_info = None
    
    # --------------------------------------------------------------------------
    
    def send(self, data):
        """
        Envia dados pelo socket. Deve ser utilizado apenas uma chamada
        connect().
        
        :param data: dados a enviar via socket
        :type data: bytes
        """
        self.socket.send(data)

    # --------------------------------------------------------------------------
    
    def recv(self, buffer_size):
        """
        Recebe dados pelo socket.
        Bloqueante.
        Se há um client_socket no objeto, faz um recv no client_socket. Senão,
        utiliza o próprio socket.
        Lança uma exceção IOError caso a conexão seja interrompida enquanto está
        bloqueado.
        
        :param buffer_size: número de bytes máximo a receber
        :type buffer_size: int
        :return: dados recebidos
        :rtype: bytes
        """
        if self.client_socket is not None:
            return self.client_socket.recv(buffer_size)
        return self.socket.recv(buffer_size)

# ==============================================================================
