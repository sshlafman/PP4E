"""
Find the largest Python source file in an entire directory tree.
Search the Python source lib, use pprint (for "pretty print") to display results nicely.
"""
import sys, os, pprint
trace = False
if sys.platform.startswith('win'):
    dirname = r'D:\home\sshlafman\Programs\Python33\Lib'  # Windows
else:
    dirname = '/usr/lib/python'                           # Unix, Linux, Cygwin
    
allsizes = []
for (thisDir, subsHere, filesHere) in os.walk(dirname):
    if trace: print(thisDir)
    for filename in filesHere:
        if filename.endswith('.py'):
            if trace: print ('...', thisDir)
            if trace: print ('...', filename)
            fullname = os.path.join(thisDir, filename)
            fullsize = os.path.getsize(fullname)
            allsizes.append((fullsize, fullname))
            
allsizes.sort()
pprint.pprint(allsizes[:2])
pprint.pprint(allsizes[-2:])