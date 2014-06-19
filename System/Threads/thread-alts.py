import _thread, time

def action(i):
    print (i ** 3)

class Power:
    def __init__(self, i):
        self.i = i
    def action(self):
        print (self.i ** 3)

_thread.start_new_thread(action, (2,))

_thread.start_new_thread((lambda: action(2)), ())

obj = Power(2)
_thread.start_new_thread(obj.action, ())

time.sleep (3)
