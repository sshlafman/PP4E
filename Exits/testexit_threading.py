import threading, sys, time
existat = 0

def action():
    sys.exit() # or raise SystemExit
    print('not reached')
    
threading.Thread(target=action).start()
time.sleep(2)
print('Main exit')