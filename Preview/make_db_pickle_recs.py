#!/usr/bin/env python3
from initdata import sue, bob, tom
import pickle
for (key, record) in [('bob', bob),('sue', sue),('tom', tom)]:
    recfile = open(key + '.pkl', 'wb')
    pickle.dump(record,recfile)
    recfile.close()
