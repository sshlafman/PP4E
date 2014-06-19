#!/usr/bin/env python3
from initdata import db
import pickle
dbfile = open ('people-pickle', 'wb')
pickle.dump(db,dbfile)
dbfile.close()

