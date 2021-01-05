import threading
import time

exitFlag = 0
threadingLock = threading.Lock()
threads = []

class CreateThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        # Get lock to synchronize threads
        threadingLock.acquire()
        print_time(self.name, 5, self.counter)
        # Free lock to release next thread
        threadingLock.release()
        print("Exiting " + self.name)


def print_time(threadName, counter, delay):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print(f"{threadName}: {time.ctime(time.time())}")
        counter -= 1


# Create new threads
thread1 = CreateThread(1, 'Thread-1', 1)
thread2 = CreateThread(2, 'Thread-2', 2)

# Start new threads
thread1.start()
thread2.start()

# Add threads to thread List
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()

print("Exiting Main Thread")