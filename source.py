#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import socket
import sys
import time
from threading import Thread
import struct

# Convert given integer to byte format
def packetize(num):
    return struct.pack("<i",num)

# Convert given byte to integer tuple
# First value of the returned tuple is the value
def unpacketize(packet):
    return struct.unpack("<i",packet)[0]

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

FILE = sys.argv[1]
f = open(FILE,"r") # open file to be sent over the network



seq_num = 0 # Initialize sequence number

while True: # load file to the packets list
    payload = f.read(504)
    if not payload:
        break

    s_num = packetize(seq_num) # conver sequence number to string
    checksum = packetize(internet_checksum(payload)) # Calculate checksum of the payload and convert it into string
    
    # packetize header + payload 
    packets.append(s_num + checksum + payload)   

    seq_num +=1 # increment sequence number by one


num_packets = len(packets) # number of packets 

f.close() # after finishing reading file, close file...


acked = False # flag
base = 0 # set base 
next_to_send = 0 # sequence number of the next message
WINDOW_SIZE = 4 #set windows size

class sender(Thread):
    def __init__(self): 
	    Thread.__init__(self)
        
    def run(self):
        global base,acked,WINDOW_SIZE,next_to_send # make these variables global

        TIMEOUT = WINDOW_SIZE / 4 #set timeout variable
        
        
        while base < num_packets: #main loop

            while next_to_send < base + WINDOW_SIZE: 
                try:
                    s.send(packets[next_to_send]) # send messages to broker
                except IndexError:
                    break
                else:
                    next_to_send += 1 # increment 
                

            start = time.time()

            # Wait for timeout or to be acked
            while time.time() - start < TIMEOUT and not acked:
                time.sleep(0.05)
            
            # if not received ack
            if not acked:
                next_to_send = base
            else:
                WINDOW_SIZE =  min(WINDOW_SIZE, num_packets - base) # configuration for last 4(WINDOW SIZE) messages
                acked = False # make acked flag false

        
        final_message = packetize(-1) # Send seq_number = -1 as terminator
        s.send(final_message) # send message to broker
        base = num_packets
        print("Closing sender Thread")

       

class receiver(Thread):
    def __init__(self): 
	    Thread.__init__(self)
    
    def run(self):
        global base,acked

        while True:
            rcv_data = s.recv(4) # receive destination reply (i.e. ACK)
            ack_number = unpacketize(rcv_data) # get ack number
            
            if(ack_number + WINDOW_SIZE >= base):
                print('ack number:',ack_number)
                base = ack_number + 1
                acked = True
            
            # If receive the last ack close thread
            if(ack_number == num_packets-1):
                print("Last ack message received:",num_packets-1)
                print("Closing receiver Thread")
                break


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


