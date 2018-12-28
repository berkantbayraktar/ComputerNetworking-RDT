#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import socket
from random import randint
import struct

def unpacketize(packet):
    return struct.unpack("<i",packet)[0]


if __name__ == '__main__': 

    broker_ip_1 = '10.10.1.2' # broker ip-1 assigned as a receiver of destination over router 1
    broker_ip_2 = '10.10.2.1' # broker ip-2 assigned as a receiver of destination over router 2
    destination_ip_1 = '10.10.3.2' # destination ip-1   ASSIGNED FOR ROUTE BROKER-> ROUTER_1 -> DESTINATION
    destination_ip_2 =  '10.10.5.2' #destination ip-2   ASSIGNED FOR ROUTE BROKER-> ROUTER_2 -> DESTINATION
    tcp_port = 25574 # port number for receiving
    udp1_port = 19077 # port number for sending to destination via router_1  
    udp2_port = 19078 # port number for sending to destination via router_2

    # create TCP socket for source
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((broker_ip_1, tcp_port))
    # start listening source
    tcp_socket.listen(1)
    conn,addr = tcp_socket.accept()

    
    udp_socket_d1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create UDP socket between broker and destination 
    udp_socket_d2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create UDP socket between broker and destination
    udp_socket_d1.bind((broker_ip_1,udp1_port)) # bind udp socket between broker and destination 
    udp_socket_d2.bind((broker_ip_2,udp2_port)) # bind udp socket between broker and destination 
    udp_socket_d1.settimeout(0.05) # set socket timeout to 50ms
    udp_socket_d2.settimeout(0.05) # set socket timeout to 50ms
    rand = randint(0, 1) # generate random number 0 or 1.

    while 1 : 
        
        
        data = conn.recv(512) # receive 512 bytes data from source 
        seq_number = unpacketize(data[:4]) # get seq number of the packet
        
        #if data is valid
        if data : 
            
            # if random number is 1 send to destination via router_1
            if rand == 1 : 
                # send message to destination via router_1
                udp_socket_d1.sendto(data,(destination_ip_1,udp1_port))
                if(seq_number == -1): # after the file is transferred succesfully, we send empty message from destination which has seq number = 1 to be able to close scripts.
                    exit(0)
                try:    
                    # receive destination reply from destination via router_1
                    rcv_msg_r1,addr_r1 = udp_socket_d1.recvfrom(4)
                except socket.timeout:
                    print('TIMEOUT')
                    rand = 0 # makes rand = 0 from 1
                
                else:
                    # send reply to source node
                    conn.sendall(rcv_msg_r1)
                    rand = 0  # makes rand = 0 from 1
                
            # otherwise send to destination via router_2
            elif rand == 0: 
                # send message to destination via router_2
                udp_socket_d2.sendto(data,(destination_ip_2,udp2_port))
                if(seq_number == -1): # after the file is transferred succesfully, we send empty message from destination which has seq number = 1 to be able to close scripts.
                    exit(0)
                try:
                    # receive destination reply from destination via router_2
                    rcv_msg_r2,addr_r2 = udp_socket_d2.recvfrom(4)
                except socket.timeout:
                    print('TIMEOUT')
                    rand  = 1 # makes rand = 1 from 0 
                else:
                    # send reply to source node
                    conn.sendall(rcv_msg_r2)
                    rand = 1 # makes rand = 1 from 0 
                

    # close tcp connection
    conn.close()  
