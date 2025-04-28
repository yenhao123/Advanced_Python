import threading
import time

def worker():
    print(f"Thread {threading.current_thread().name} starts")
    time.sleep(2)
    print(f"Thread {threading.current_thread().name} ends")

if __name__ == "__main__":
    t1 = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Main thread ends")