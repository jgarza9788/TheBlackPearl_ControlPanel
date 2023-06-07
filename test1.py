from threading import Thread
import time 

def func1():
    print('func1_Start')
    print('func1_Working')
    time.sleep(5)
    print('func1_End')

def func2():
    print('func2_Start')
    print('func2_Working')
    time.sleep(0)
    print('func2_End')

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()