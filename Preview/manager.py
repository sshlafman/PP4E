#!/usr/bin/env python3
from person import Person

class Manager(Person):
    def __init__(self, name, age, pay):
        Person.__init__ (self, name, age, pay, 'manager')

    def giveRaise(self, percent, bonus=0.1):
        Person.giveRaise(self, percent + bonus)

if __name__ == '__main__':
    tom = Manager('Tom Doe', age=50, pay=50000)
    print(tom.lastName())
    tom.giveRaise(.20)
    print(tom.pay)
    print(tom)
