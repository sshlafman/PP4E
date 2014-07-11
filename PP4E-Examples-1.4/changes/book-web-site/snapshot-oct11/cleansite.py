"""
=======================================================================
use python's html and url parser libs to try to isolate and move
unused files in a web site directory;  run me in the directory of
the site's root html file(s) (default=[index.html]); 

this is heuristic: it assumes that referenced files are in this site 
if they exist here;  it also may incorrectly classify some files as 
unused if they are referenced only from files which cause Python's
html parser to fail -- you should inspect the run log and unused file
directory manually after a run, to see if parse failures occurred;
more lenient html parsers exist for Python, but all seem 2.X-only; 
other parse options might avoid failures too: re.findall() pattern 
matches for '(?s)href="(.*?)"' and 'src=...'? (see Example 19-9);

see chapters 19 and 14 for html parsers, chapter 13 for url parsing;
to do: extend me to delete the unused files from remote site via ftp:
not done because unused files require verification if parse failures;
caveat: assumes site is one dir, doesn't handle subdirs (improve me);
=======================================================================
"""

import os, sys, html.parser, urllib.parse

def findUnusedFiles(rootfiles=['index.html'], dirunused='Unused', skipfiles=[]):
    """
    find and move files referenced by rootfiles and by any html they 
    reach, ignoring any in skipfiles, and moving unused to dirunused;
    """
    usedFiles = set(rootfiles)
    for rootfile in rootfiles:
        parseFileRefs(rootfile, usedFiles, skipfiles, 0)
    moveUnusedFiles(usedFiles, dirunused)
    return usedFiles

def moveUnusedFiles(usedFiles, dirunused, trace=print): 
    """
    move unused files to a temp directory
    """
    print('-' * 80)
    if not os.path.exists(dirunused):               # tbd: clean if present?
        os.mkdir(dirunused)
    for filename in os.listdir('.'):
        if filename not in usedFiles:
            if not os.path.isfile(filename):
                print('Not a file:', filename)
            else:
                trace('Moving...', filename)
                os.rename(filename, os.path.join(dirunused, filename))

def parseFileRefs(htmlfile, usedFiles, skipFiles, indent, trace=print):
    """
    find files referenced in root, recur for html files
    """
    trace('%sParsing:' % ('.' * indent), htmlfile)
    parser = MyParser(usedFiles, skipFiles, indent)
    text   = open(htmlfile).read()
    try:
        parser.feed(text)
    except html.parser.HTMLParseError as E:
        print('==>FAILED:', E)                   # file's refs may be missed!
    parser.close()

class MyParser(html.parser.HTMLParser):
    """
    use Python stdlib html parser to scan files; could nest this in 
    parseFileRefs for enclosing scope, but would remake class per call;
    """
    def __init__(self, usedFiles, skipFiles, indent):
        self.usedFiles = usedFiles
        self.skipFiles = skipFiles
        self.indent    = indent
        super().__init__()           # vs html.parser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        """
        callback on tag open during parse: check links and images
        """
        if tag == 'a':
            url = [value for (name, value) in attrs if name.lower() == 'href']
            if url:
                self.notefile(url[0])

        elif tag == 'img':
            url = [value for (name, value) in attrs if name.lower() == 'src']
            if url:
                self.notefile(url[0])

    def notefile(self, url):
        """
        note used file found, and recur to a nested parse if html
        """
        urlparts = urllib.parse.urlparse(url)
        (scheme, server, filepath, parms, query, frag) = urlparts
        filename = os.path.basename(filepath)

        if (os.path.exists(filename)       and                # is it here?
            filename not in self.skipFiles and                # ignore it?
            filename not in self.usedFiles):                  # skip repeats?

            self.usedFiles.add(filename)                      # add in-place
            if filename.endswith(('.html', '.htm')):          # recur for html
                parseFileRefs(
                    filename, self.usedFiles, self.skipFiles, self.indent + 3)

def deleteUnusedRemote(localUnusedDir, ftpsite, ftpuser, ftppswd, ftpdir='.'):
    """
    to do: delete unused files from remote site too? see Chapter 13 for ftp;
    not used because unused dir requires manual inspection if parse failures
    """   
    from ftplib import FTP
    connection = FTP(ftpsite)
    connection.login(ftpuser, ftppswd)
    connection.cwd(ftpdir) 
    for filename in os.listdir(localUnusedDir):
        connection.delete(filename)

if __name__== '__main__':
    htmlroot = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
    moveto   = sys.argv[2] if len(sys.argv) > 2 else 'PossiblyUnused'
    ignore   = sys.argv[3] if len(sys.argv) > 3 else 'whatsnew.html'
    usedFiles = findUnusedFiles([htmlroot], moveto, [ignore])
    moveFiles = os.listdir(moveto)
 
    print('-' * 80)
    print('**Summary**\n')
    print('%d unused files moved to:\n\t%s\n' % 
              (len(moveFiles), os.path.abspath(moveto)))
    print('%d used files in this site: ' % len(usedFiles))
    for F in sorted(usedFiles): print('\t', F)

    """
    if input('delete remotely?') in 'yY':
        deleteUnusedRemote(moveto, input('site?'), input('user?'), input('pswd?'))
    """
