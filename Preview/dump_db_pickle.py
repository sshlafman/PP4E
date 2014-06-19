#!/usr/bin/env python3
import pickle
dbfile = open('people-pickle','rb')
db = pickle.load(dbfile)
for key in db:
    print(key, '=>', db[key])
print(db['sue']['name'])
