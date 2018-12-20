#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
from random import randint


broker_ip = '10.10.1.2' # broker ip
router_ip_1 = '10.10.3.2' # destination ip
router_ip_2 = '10.10.3.2' # destination ip
tcp_port = 25574 # port number for receiving
udp1_port = 19077 # port number for sending to router1
udp2_port = 25570 # port number for sending to router2

# create TCP socket for source
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((broker_ip, tcp_port))
# start listening source
tcp_socket.listen(1)
conn,addr = tcp_socket.accept()

# create socket for router1 and router2
udp_socket_r1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket_r2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket_r1.bind((broker_ip,udp1_port))
udp_socket_r2.bind((broker_ip,udp2_port))

while 1 : 
    
    # receive 1024 bytes data from source 
    data = conn.recv(1024)

    #if data is valid
    if data : 
        # pick either 0 or 1 for deciding which router to send
        rand = randint(0, 1)
        # if random number is 1 send to router1 
        if rand == 1 : 
            # send message to router1
            udp_socket_r1.sendto(data,(router_ip_1,udp1_port))
            # receive destination reply from router1 
            rcv_msg_r1,addr_r1 = udp_socket_r1.recvfrom(1024)
            # send reply to source
            conn.sendall(rcv_msg_r1)
            
        # otherwise send to router2
        else :
             # send message to router2
            udp_socket_r2.sendto(data,(router_ip_2,udp2_port))
            # receive destination reply from router2
            rcv_msg_r2,addr_r2 = udp_socket_r2.recvfrom(1024)
             # send reply to source
            conn.sendall(rcv_msg_r2)
            

# close tcp connection
conn.close()  
