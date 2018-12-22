#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import socket
import sys
import time
from threading import Thread
import struct

# Convert given integer to byte format
def packetize(num):
    return struct.pack("<I",num)

# Convert given byte to integer tuple
# First value of the returned tuple is the value
def unpacketize(packet):
    return struct.unpack("<I",packet)[0]

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



packets = []



HOST = '10.10.1.2' # broker ip
PORT = 25574  # port number 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
s.connect((HOST,PORT)) # connect

f = open("./demofile.txt","r") # open file to be sent over the network



seq_num = 0 # Initialize sequence number

while True: # load file to the packets list
    payload = f.read(504)
    if not payload:
        break

    s_num = packetize(seq_num) # conver sequence number to string
    #seq_length = str(len(s_num)) # calculate length of the sequence number string
    checksum = packetize(internet_checksum(payload)) # Calculate checksum of the payload and convert it into string
    #checksum_length = str(len(checksum_string)) # length of checksum
    
    # packetize header + payload 
    packets.append(s_num + checksum + payload)   

    seq_num +=1 # increment sequence number by one


num_packets = len(packets)

f.close() # after finishing reading file, close file...


acked = False
base = 0
next_to_send = 0
WINDOW_SIZE = 4

class sender(Thread):
    def __init__(self): 
	    Thread.__init__(self)
        
    def run(self):
        global base,acked,WINDOW_SIZE,next_to_send

        TIMEOUT = WINDOW_SIZE / 4
        
        
        while base < num_packets:

            while next_to_send < base + WINDOW_SIZE:
                s.send(packets[next_to_send])
                next_to_send += 1

            start = time.time()

            # Wait for timeout or to be acked
            while time.time() - start < TIMEOUT and not acked:
                time.sleep(0.05)
                #print('time diff : ', time.time() - start)
            
            # if not received ack
            if not acked:
                next_to_send = base
            else:
                WINDOW_SIZE =  min(WINDOW_SIZE, num_packets - base)
                acked = False

class receiver(Thread):
    def __init__(self): 
	    Thread.__init__(self)
    
    def run(self):
        global base,acked

        while True:
            rcv_data = s.recv(4) # receive destination reply (i.e. ACK)
            print(len(rcv_data))
            print rcv_data
            ack_number = unpacketize(rcv_data) # get ack number
            
            if(ack_number >= base):
                print('ack number:',ack_number)
                base = ack_number + 1
                acked = True


if __name__ == '__main__': 

    # create thread for sending
    src_snd_thread = sender()
    
    # create thread for receiving
    src_rcv_thread = receiver()

# Start running the threads
	
    src_snd_thread.start()
    src_rcv_thread.start()

# Close threads
    src_snd_thread.join()
    src_rcv_thread.join()


# close tcp socket
s.close()

