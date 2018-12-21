from threading import Thread,Lock

lock = Lock()
ilker = 5


class send(Thread):
    global ilker
    def __init__(self): 
	    Thread.__init__(self)
        

    def run(self):
        lock.acquire()
        ilker = 6
        lock.release()

class receive(Thread):
    global ilker
    def __init__(self): 
	    Thread.__init__(self)
    
    def run(self):
        while True:
            print(ilker)




if __name__ == '__main__': 

    # create thread for sending
    t1 = send()
    
    # create thread for receiving
    t2 = receive()

# Start running the threads
	
    t1.start()
    t2.start()

# Close threads
    t1.join()
    t2.join()