
from time import sleep

from threading import Thread



def run(index):
    print("This is "+index)
    sleep(20)
    print(index+" end")
    
if __name__ == '__main__':
    thread1= Thread(target=run,args=('1'))
    thread1.start()
    thread2= Thread(target=run,args=('2'))
    thread2.start()

