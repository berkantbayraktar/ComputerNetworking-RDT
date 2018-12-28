#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import socket
from threading import Thread
import time
import struct

# Convert given integer to byte format
def packetize(num):
    return struct.pack("<i",num)

# Convert given byte to integer tuple
# First value of the returned tuple is the value
def unpacketize(packet):
    return struct.unpack("<i",packet)[0]

FILE = open("output.txt","w")
broker_ip_1 = '10.10.1.2' # broker ip-1
broker_ip_2 = '10.10.2.1' # broker ip-2
dest_ip_1 = '10.10.3.2' # IP adddress of the destination node
dest_ip_2 = '10.10.5.2' # IP adddress of the destination node
b1_port = 19077 # port number for receiving data from broker over router 1
b2_port = 19078 # port number for receiving data from broker over router 2

# create and bind socket for receiving data from broker over router1
b1_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
b1_udp_sock.bind((dest_ip_1,b1_port))

# create and bind socket for receiving data from broker over router2
b2_udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
b2_udp_sock.bind((dest_ip_2,b2_port))
expected_seq = 0 # expected sequence number for next packet
isRunning = True # flag to able to understand transferring of file is finished or not
b1_udp_sock.settimeout(3) # set timeout
b2_udp_sock.settimeout(3) # set timeout

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
        #make these variables global for both thread-1 and thread-2
        global expected_seq
        global isRunning

        if(self.PORT == 19077):  # if the packet comes from broker over router1
            while 1:
                # receive 512 byte data from router1
                try :
                    self.data,self.addr = b1_udp_sock.recvfrom(512)
                except:
                    if not isRunning:  # close thread-1 if the file transfer is completed
                        print('Destination Thread-1 Closing')
                        break
                else:           
                    seq_number = unpacketize(self.data[:4]) # get sequence number of packet
                    if(seq_number != -1): # if the transfer of the file is not completed
                        checksum = unpacketize(self.data[4:8]) # get checksum of the packet

                        payload = self.data[8:] # get actual message from packet
                        flag = internet_checksum(payload,checksum)  # calculate checksum flag

                        if seq_number == expected_seq and flag == 0:
                            FILE.write(payload) # write payload part of the packet to file     
                            ack_message = packetize(expected_seq)  # packetize ack message                         
                            b1_udp_sock.sendto(ack_message,(broker_ip_1,self.PORT)) # send cumulative ack to broker over r1
                            expected_seq += 1 # increment expected sequence
                            

                        else:
                            # packetize ack message
                            ack_message = packetize(expected_seq - 1)
                            b1_udp_sock.sendto(ack_message,(broker_ip_1,self.PORT))  # send ack message to broker over r1           
                    
                        # print received message
                        print('seq_number: ',seq_number,'checksum: ',checksum, 'flag: ',flag)
                    
                    # Exit
                    else: # if the transfer of the file is completed
                        isRunning = False
                        print("Closing file")
                        FILE.close() #close file
                        print('Destination Thread-1 Closing')
                        break # break main loop and close thread
                
                 
                    
        else:    # if the packet comes from broker over router2
            while 1:
                try:
                    # receive 1000 byte data from router1
                    self.data,self.addr = b2_udp_sock.recvfrom(512)

                except:
                    if not isRunning: # close thread-2 if the file transfer is completed
                        print('Destination Thread-2 Closing')
                        break

                else:      
                    seq_number = unpacketize(self.data[:4]) # get sequence number of packet
                    if(seq_number != -1): # if the transfer of the file is not completed
                        checksum = unpacketize(self.data[4:8]) # get checksum of the packet

                        payload = self.data[8:] # get actual message from packet
                        
                        flag = internet_checksum(payload,checksum)  # calculate checksum flag
                        
                        if seq_number == expected_seq and flag == 0:
                            FILE.write(payload) # write payload part of the packet to file     
                            ack_message = packetize(expected_seq) # packetize ack message             
                            b2_udp_sock.sendto(ack_message,(broker_ip_2,self.PORT)) # send cumulative ack to broker 
                            expected_seq += 1 # increment expected sequence
                            

                        else:                       
                            ack_message = packetize(expected_seq - 1) # packetize ack message
                            b2_udp_sock.sendto(ack_message,(broker_ip_2,self.PORT))   # send ack message to broker over r2                        
                    
                        #print received message
                        print('seq_number: ',seq_number,'checksum: ',checksum, 'flag: ',flag)
                    
                    # Exit
                    else: # if the transfer of the file is completed
                        isRunning = False
                        print("Closing file")
                        FILE.close() #close file
                        print('Destination Thread-2 Closing')                
                        break # break main loop and close thread



if __name__ == '__main__': 

    # create thread for listening broker over router1
    Thread_b1 = myThread(dest_ip_1, b1_port)
    
    # create thread for listening broker over router2
    Thread_b2 = myThread(dest_ip_2, b2_port)

# Start running the threads
	
    Thread_b1.start()
    Thread_b2.start()

# Close threads
    Thread_b1.join()
    Thread_b2.join()
