from threading import Thread
import time

def wait(x):
    time.sleep(5)
    print(x)

# Thread(target=wait, args=[1]).start()
# t.run()

Thread(name='background_monitor', target=wait,args=[1]).start()

print(100)
print(99)
print(98)