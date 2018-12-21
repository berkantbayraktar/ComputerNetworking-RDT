#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import socket
import sys
import time
from threading import Thread

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


base = 0
WINDOW_SIZE = 4
SEGMENT_SIZE = 512
TIMEOUT = WINDOW_SIZE / 4

HOST = '10.10.1.2' # broker ip
PORT = 25574  # port number 

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect
s.connect((HOST,PORT))

# open file to be sent over the network
f = open("./demofile.txt","r")


# Initialize sequence number
seq_num = 0
# load file to the packets list
while True:
    payload = f.read(450)
    if not payload:
        break

    s_num = str(seq_num)
    seq_length = str(len(s_num))
    checksum_string = str(internet_checksum(payload)) # Calculate checksum of the packet and convert it into string
    checksum_length = str(len(checksum_string)) # length of checksum
    
    packets.append(seq_length + s_num
    + checksum_length + checksum_string
    + payload)

num_packets = len(packets)

# close file
f.close()


acked = False

class sender(Thread):
    def __init__(self): 
	    Thread.__init__(self)

        
    def run(self):
  
        next_to_send = 0
        
        while base < num_packets:

            while next_to_send < base + WINDOW_SIZE:
                s.send(packets[next_to_send])
                next_to_send += 1

            start = time.time()

            # Wait for timeout or to be acked
            while time.time() - start < TIMEOUT and not acked:
                time.sleep(0.05)
            
            # if not received ack
            if not acked:
                next_to_send = base
            else:
                WINDOW_SIZE =  min(WINDOW_SIZE, num_packets - base)

class receiver(Thread):
    def __init__(self): 
	    Thread.__init__(self)
    
    def run(self):
        
        while True:
            rcv_data = s.recv(50) # receive destination reply from broker
            ack_number = int(rcv_data) # convert time string to float
            
            if(ack_number >= base):
                base = ack_number + 1


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

