#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
from random import randint


broker_ip_1 = '10.10.1.2' # broker ip
broker_ip_2 = '10.10.2.1' # broker ip
destination_ip_1 = '10.10.3.2'
destination_ip_2 =  '10.10.5.2'
tcp_port = 25574 # port number for receiving
udp1_port = 19077 # port number for sending to router1
udp2_port = 19078 # port number for sending to router2

# create TCP socket for source
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((broker_ip_1, tcp_port))
# start listening source
tcp_socket.listen(1)
conn,addr = tcp_socket.accept()

# create socket for router1 and router2
udp_socket_r1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket_r2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket_r1.bind((broker_ip_1,udp1_port))
udp_socket_r2.bind((broker_ip_2,udp2_port))
rand = randint(0, 1)

while 1 : 
    
    # receive 512 bytes data from source 
    data = conn.recv(512)

    #if data is valid
    if data : 
        # pick either 0 or 1 for deciding which router to send
        
        # if random number is 1 send to router1 
        print('rand:',rand)
        if rand == 1 : 
            # send message to router1
            udp_socket_r1.sendto(data,(destination_ip_1,udp1_port))
            # receive destination reply from router1 
            rcv_msg_r1,addr_r1 = udp_socket_r1.recvfrom(512)
            # send reply to source
            conn.sendall(rcv_msg_r1)
            rand = 0
            
        # otherwise send to router2
        elif rand == 0:
             # send message to router2
            udp_socket_r2.sendto(data,(destination_ip_2,udp2_port))
            # receive destination reply from router2
            rcv_msg_r2,addr_r2 = udp_socket_r2.recvfrom(512)
             # send reply to source
            conn.sendall(rcv_msg_r2)
            rand = 1
            

# close tcp connection
conn.close()  
