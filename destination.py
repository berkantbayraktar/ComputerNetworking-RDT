#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
from threading import Thread
import time
import struct

# Convert given integer to byte format
def packetize(num):
    return struct.pack("<I",num)

# Convert given byte to integer tuple
# First value of the returned tuple is the value
def unpacketize(packet):
    return struct.unpack("<I",packet)[0]

FILE = open("output.txt","w")
broker_ip_1 = '10.10.1.2' # broker ip
broker_ip_2 = '10.10.2.1' # broker ip
dest_ip_1 = '10.10.3.2' # IP adddress of the destination node
dest_ip_2 = '10.10.5.2' # IP adddress of the destination node
r1_port = 19077 # port number for receiving data from r1
r2_port = 19078 # port number for receiving data from r2

# create and bind socket for receiving data from router1
r1_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r1_udp_sock.bind((dest_ip_1,r1_port))

# create and bind socket for receiving data from router2
r2_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
r2_udp_sock.bind((dest_ip_2,r2_port))
expected_seq = 0

def internet_checksum(data, sum=0):
    for i in range(0,len(data),2):
        if i + 1 >= len(data):
            sum += ord(data[i]) & 0xFF
        else:
            w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i+1]) & 0xFF)
            sum += w

    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)

    sum = ~sum

    return sum & 0xFFFF



class myThread(Thread): # Thread class 

    #constructor for thread , construct with host and port number
    def __init__(self, HOST, PORT): 
	    Thread.__init__(self)
	    self.HOST = HOST
	    self.PORT = PORT       
    
    def run(self):
        
        global expected_seq

        if(self.PORT == 19077):  # if port number reserved for router1
            while 1:
                # receive 1000 byte data from router1
                self.data,self.addr = r1_udp_sock.recvfrom(512)
                # if received data is valid
                if self.data:
                    
                    seq_number = unpacketize(self.data[:4])
                    checksum = unpacketize(self.data[4:8])

                    payload = self.data[8:]
                    
                    flag = internet_checksum(payload,checksum)  

                    if seq_number == expected_seq and flag == 0:
                        print(payload)
                        FILE.write(payload)
                        # packetize ack message
                        ack_message = packetize(expected_seq)
                        # send cumulative ack to broker 
                        r1_udp_sock.sendto(ack_message,(broker_ip_1,self.PORT))
                        # increment expected sequence
                        expected_seq += 1
                        

                    else:
                        # packetize ack message
                        ack_message = packetize(expected_seq - 1)
                        r2_udp_sock.sendto(ack_message,(broker_ip_1,self.PORT))             
                   
                    # print received message
                    print('seq_number: ',seq_number,'checksum: ',checksum, 'flag: ',flag)
                
                # if end of the file
                else :
                    break
                 
                    
        else:   #if port number reserved for router2
            while 1:
                # receive 1000 byte data from router1
                self.data,self.addr = r2_udp_sock.recvfrom(512)
                # if received data is valid
                if self.data:
        
                    seq_number = unpacketize(self.data[:4])
                    checksum = unpacketize(self.data[4:8])

                    payload = self.data[8:]
                    
                    flag = internet_checksum(payload,checksum)  
                    
                    if seq_number == expected_seq and flag == 0:
                        print(payload)
                        FILE.write(payload)
                        # packetize ack message
                        ack_message = packetize(expected_seq)
                        # send cumulative ack to broker 
                        r2_udp_sock.sendto(ack_message,(broker_ip_2,self.PORT))
                        expected_seq += 1
                        

                    else:
                        # packetize ack message
                        ack_message = packetize(expected_seq - 1)
                        r2_udp_sock.sendto(ack_message,(broker_ip_2,self.PORT))                
                   
                    #print received message
                    print('seq_number: ',seq_number,'checksum: ',checksum, 'flag: ',flag)
                
                # if end of the file
                else:
                    break
                    
        
                    




if __name__ == '__main__': 

    # create thread for router1 socket
    Thread_r1 = myThread(dest_ip_1, r1_port)
    
    # create thread for router2 socket
    Thread_r2 = myThread(dest_ip_2, r2_port)

# Start running the threads
	
    Thread_r1.start()
    Thread_r2.start()

# Close threads
    Thread_r1.join()
    Thread_r2.join()
# Close file
    FILE.close()
