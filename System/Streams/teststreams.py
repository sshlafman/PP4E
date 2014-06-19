"read numbers till eof and show squares"

def interact():
    print('Hello stream world')
    while True:
        try:
            reply = input('Enter a number>')
        except EOFError:
            break
        else:
            num = int(reply)
            print ("%d squared is %d" % (num, num ** 2))
    print("Bye")

if __name__ == '__main__':
    interact()
