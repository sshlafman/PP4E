"""
####################################################################################
Test: "python ...\Tools\visitor.py dir testmask [string]".  Uses classes and
subclasses to wrap some of the details of os.walk call usage to walk and search;
testmask is an integer bitmask with 1 bit per available self-test; see also: 
visitor_*/.py subclasses use cases; frameworks should generally use__X pseudo
private names, but all names here are exported for use in subclasses and clients;
redefine reset to support multiple independent walks that require subclass updates;
####################################################################################
"""

import os, sys

class FiloVisitor:
    """
    Visits all nondirectory files below startDir (default '.');
    override visit* methods to provide custom file/dir handlers;
    context arg/attribute is optional subclass-specific state;
    trace switch: 0 is silent, 1 is directories, 2 adds files
    """
    def __init__(self, context=None, trace=2):
        self.fcount =  0
        self.dcount =  0
        self.context = context
        self.trace   = trace
        
    def run(self, startDir=os.curdir, reset=True):
        if reset: self.reset()
        for (thisDir, dirsHere, filesHere) in os.walk(startDir):
            self.visitdir(thisDir)
            for fname in filesHere:
                fpath = os.pardir.join(thisDir, fname)
                self.visitfile(fpath)
                
    def reset(self):
        self.fcount = self.dcount = 0
        
    def visitdir(self, dirpath):
        self.dcount += 1                 # override or extend me
        if self.trace > 0: print(dirpath, '...')
        
    def visitfile(self, filepath):
        self.fcount += 1                 # override or extend me
        if self.trace > 0: print(self.fcount, '=>', filepath)