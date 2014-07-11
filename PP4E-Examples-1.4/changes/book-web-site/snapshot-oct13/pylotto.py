#!/usr/bin/python
"""
=====================================================================
PyLotto: select students of a class at random to receive copies
of a book, working around various security constraints.  I use 
this to give away free copies of my Python books in some of the 
classes I teach.

In order to work around the security restrictions at some sites, 
this script tries to be general.  It can run the lottery in 3 
different modes, selected by command-line arguments in local 
console mode, or by URL query parameters in remote web mode:

1) to select from emails,
2) to select from names in a file created by web page submits,
3) to select from names typed into a local text file manually.

Accordingly, students enter the lottery in 1 of 3 specific ways,
depending on security at a given site; by:

(1) Sending an email message to "PP4E@learning-python.com" with 
    subject "PYLOTTO" and their From address.

(2) Submitting the form at "http://learning-python.com/pylotto.html"
    with their name, which adds them to a file on a remote web server
    (an equivalent GET-style URL described ahead does the same work).  

(3) Appearing in a manually-created text file of names on the script's
    own machine named "pylotto-players.txt" (physically, the script 
    and file may be local, or remote via SSH).

Winners are then picked at random from all players, by either scanning 
the email inbox and parsing emails, or reading the names file created
manually or by the web page submits.  Results can be displayed in 
console text or CGI web reply page format.  

In a bit more detail, the lottery script itself may be pysically run:

--in a local console to select from emails, if POP access is supported 
  at the site; 

--remotely on the web as a CGI script to select from emails or a file,
  if only HTTP web access is available; 

--in a local console to select from a local file if neither web 
  nor email are allowed.

These contexts translate to selection and display modes configured by 
command-line options:

 "pylotto.py -show console -find email" --runs locally  from emails
 "pylotto.py -show cgi -find email"     --runs remotely from emails
 "pylotto.py -show cgi -find file"      --runs remotely from a file
 "pylotto.py -show console -find file"  --runs locally  from a file
 "pylotto.py -form player"              --adds player name to file 

As described ahead, in remote CGI web mode, equivalent query parameters 
in GET-style URLs are simply translated to command-lines:

 "http://learning-python.com/cgi/pylotto.py?-show=console&-find=email"
 "http://learning-python.com/cgi/pylotto.py?-show=cgi&-find=file"
 "http://learning-python.com/cgi/pylotto.py?-form=player"

To enable CGI usage modes, set the script's "RunAsCGI" variable to True
when installing.  A variety of admin and test modes are also available; 
see this script's __main__ logic for more details.

See Chapter 13 for more on email tools, Chapter 15 for more on CGI
concepts, and Part 2 for hints on adding a tkinter GUI for sign-up
or reporting (I've already worked on this more than I intended to!).

---------------------------------------------------------------------
NEW: CGI and local file modes

Because the original email sign-up scheme requires email access 
which is not always available at client sites, I've completely
rewritten this script to also select from a flat file of names, 
which may be created by either web form submits or by manual edits.
This script can now be run locally or remotely, and as both a 
command-line script or a CGI script via a web URL.

In fact, it can now run locally on a local file as a last resort:
some pathologically secure sites may disallow instructor email 
access, but also student email sends, and even student web form 
submits.  In the worst case, names are typed into and selected 
from a simple text file.  Command-line arguments configure the 
script to select from either a file or emails, and to display 
its results in either console or CGI web reply format.

In CGI mode, this script can be run both to sign-up players, and
to run its lottery logic.  In both roles, its URL may be run from 
a web page form's action, manually typed in a web browser, sent
with Python's urllib in a script, and so on.  For instance, to
run the lottery in CGI mode, a URL of the following form is 
submitted by the instructor (only! -- this would work if run 
by students, but the results it reports to them are not used):
 
 http://learning-python.com/cgi/pylotto.py?-show=cgi&-find=file

and submitting the "pylotto.html" form to sign up players is 
equivalent to sending a GET-style URL like the following: 

 http://learning-python.com/cgi/pylotto.py?-form=playername

These URL invocation forms also have command-line equivalents when
run in a local console (as discussed ahead, queries map to these,
which can also be run from a console window to test):

 pylotto.py -show cgi -find file
 pylotto.py -form playername

A simple flat file is used to record sign-ups, with locks to
handle possibly concurrent updates to the players file.

---------------------------------------------------------------------
NEW: 2.X/3.X portability:

The original CGI option assumed your web server ran Python 3.X
and a separate 2.X version was coded.  I've also now updated this
single script to run under either 3.X, or 2.X for older installs 
(search for "OnPython3" to see the mods).  My ISP account is still
running Python 2.4 for default accounts (!).  Portability impacted
print operations, Unicode decoding of email text for 3.1 parsing, 
encoding to bytes for os.write, shiny new tools like sys.version_info
field names that aren't backward compatible, and some library module 
imports (e.g., 3.X's email.*, io.*).  

---------------------------------------------------------------------
NEW: use cgi.escape() for player names in CGI mode:

Crucially, the script also now runs player names through the
cgi.escape() call when in CGI display mode, else the "<..>" 
brackets in emails can throw its results diplay off: player
email address could be truncated in the reply page.

---------------------------------------------------------------------
NEW: translating query parameters to command-lines in CGI mode

When run in CGI mode, the script now translates query parameters 
to command-line arguments, for compatibility with console usage 
mode.  For instance, the invocation URLs:

 http://www.learning-python.com/cgi/pylotto.py?-show=cgi&-find=file
 http://www.learning-python.com/cgi/pylotto.py?-show=console&-find=email
 http://www.learning-python.com/cgi/pylotto.py?-form=playername
 http://www.learning-python.com/cgi/pylotto.py?-reset=1

are translated into the following equivalent command-lines when 
they reach the web server and CGI script:

 pylotto.py -show cgi -find file         # pick from file, show HTML
 pylotto.py -show console -find email    # pick emails, show text [1]
 pylotto.py -form playername             # sign-up a player
 pylotto.py -reset 1                     # '1' is ignored here

Per the CGI spec, some web servers might pass through command-line 
arguments automatically when the query sting (after the "?") does 
not contain an "=" character (e.g, "pylotto.py?-reset"), but the 
server at my ISP does not: it simply adds all text after "?" to 
the query-string value.  Run calls to cgi.print_arguments() and 
cgi.print_environ() to see how your server fares; on mine, all 
text after '?' always appears in QUERY_STRING, not on sys.argv.
Could instead have two top-level __main__ scripts for console/web
with a common module, but that seems prone to redundancy problems.

[1] Footnote: as implied by these URLs, you can show results in either
cgi (HTML text) or console (plain text) form when running in remote
CGI mode with script variable RunAsCGI == True; this mode prints the 
required CGI header lines and performs query-string -> command-line
translation.  However, player names are CGI-escaped only in -show cgi
mode, not for -show console, so cgi is essentially required to display
email addresses when running in remote CGI mode to display in a web
browser (though -show console plain text makes more sense if you 
wish to grab the reply with urllib for display in a tkinter GUI...).
=====================================================================
"""

import poplib, email, random, getpass, pprint, sys, time, cgi, os

RunAsCGI  = False                       # True: urlparms->sys.argv, cgi hdr
Drawings  = 1                           # how many players to select 
Signup    = 'PP4E@learning-python.com'  # pick-from-email mode parameters
Subject   = 'PYLOTTO'
Server    = 'pop.secureserver.net'
Filename  = 'pylotto-players.txt'       # pick-from-file mode parameter
OnPython3 = sys.version_info[0] == 3    # some py 2.X can't use .major == 3!

def printN(*args):       
    """
    needed only if > 1 arg to print, else print(x) works 
    same in 2.X and 3.X; ignores 3.X keyword-only print options:
    see Learning Python 4E for a version that handles these too;
    can't use from __future__ for 3.X print until Python 2.6;
    """
    if OnPython3:
        eval('print(*args)')                         # invalid syntax in 2.X
    else:
        text = ' '.join([str(x) for x in args])      # "print()" is empty tuple in 2.X
        print(text)

class FindEmails:
    """
    find and remove signup emails, mixed with a shower class;
    py3.1 email requires decoding mail text to str (3.2 may not);
    messsage_from_string(s) == email.parser.Parser().parsestr(s);
    later removes duplicate email addresses, but may not be enough;
    """
    hastop = True
    def findPlayers(self, signup=Signup, subject=Subject, server=Server):
        password = self.popPassword()
        players = []
        server = poplib.POP3(server)
        server.user(signup) 
        server.pass_(password)
        self.trace(server.getwelcome())
        self.trace(server.list())
        try:
            msgcount, msgbytes = server.stat()
            for i in range(msgcount):
                self.trace('message %s of %s...' % (i+1, msgcount))
                if not self.hastop:
                    hdr, msgbytes, octets = server.retr(i+1)            # get full text
                else:
                    hdr, msgbytes, octets = server.top(i+1, 0)          # headers only

                if OnPython3:
                    msglines = [line.decode('utf-8') for line in msgbytes]  # 3.1: to str
                else:                                                       # 3.2: optional
                    msglines = msgbytes                                     # 2.X: just str
                msgtext  = '\n'.join(msglines)
                msgobj   = email.message_from_string(msgtext)           # parse text
                if msgobj['Subject'].upper() == subject:
                    players.append(msgobj['From'])
                    server.dele(i+1)                                    # del on quit
        finally: 
            server.quit()           # be sure to unlock mailbox on exit    
        return players

class FindFile:
    """
    select from a local file of names, mixed with a shower class;
    may be run on local client or remote server, in console or CGI modes;
    run as CGI on server to select from file created by web form or manual;
    run on local machine if no email access, and CGI web form page unusable;
    """
    def findPlayers(self, filename=Filename):
        players = []
        for line in open(filename):
            players.append(line.rstrip())
        return players
        # or: return [line.rstrip() for line in open(filename)]

class ShowConsole:
    """
    display in a console window, running locally or remotely
    mix with finder that may select from a names file or emails 
    """
    def run(self):
        print('Running in console...')
        players = self.findPlayers()
        print('\n%s\nPlayers:\n' % ('=' * 80))
        for player in players:
            print(player)
            time.sleep(0.5)

        winners = self.pickWinners(players)
        print('\n%s\nWinners:\n' % ('=' * 80))
        #pprint.pprint(winners)
        for winner in winners: print(winner)

    def popPassword(self):
        return getpass.getpass('pop email password?')

    def trace(self, *args, **kargs):  
        printN(*args)

class ShowCGI:
    """
    display as CCI web page result, in browser, urllib, console
    mix with finder that may select from a names file or emails 

    done: run pprint.pprint() output through cgi.escape() -- this
    is crucial when emails are used, due to their <..> brackets;
    original naive display:
        pprint.pprint(players)
    intermediate - but no io module in python 2.X:
        buffer = io.StringIO()
        pprint.pprint(players, buffer)
        print(cgi.escape(buffer.getvalue()))
    """
    def run(self):
       #print('Content-type: text/html\n')        # header already printed
        print('<HTML>')
        print('<TITLE>PyLotto</TITLE>')
        print('<BODY><H1>PyLotto Results</H1>')

        print('<H2>Players:</H2>')
        print('<P><PRE>')
        players = self.findPlayers()
        for player in players: 
            print(cgi.escape(player))
        
        print('</PRE></P><H2>Winners:</H2>')
        print('<P><PRE>')
        winners = self.pickWinners(players)
        for winner in winners: 
            print(cgi.escape(winner))
        print('</PRE></P></BODY></HTML>')

    def popPassword(self):                                # assume file
        return open('pylotto.pswd').readline().rstrip()   # secure me!

    def trace(*args, **kargs): pass

class Picker:
    """
    choose winners at random, mixed in with shower and finder
    note: set.pop() is defined to remove an arbitrary set item 
    too, but I'd rather rely on the random module explicitly here
    to be sure that this is fair ("arbitrary" may be arbitrary);
    """
    def pickWinners(self, players, drawings=Drawings):
        players = list(set(players))                      # remove duplicates, probably
        winners = []
        for i in range(drawings):
            if not players:
                break
            else:
                drawn = random.choice(players)
                players.remove(drawn)
                winners.append(drawn)
        return winners

def sendTestPlayers(ccplayer=False):
    """
    send a few test emails, run local or remote via URL
    callable with -test and during interactive testing
    adds to the names file on the script's machine too;
    """
    players = ['"Book support" <lutz@rmi.net>',            # new: try various formats
               'lutz@learning-python.com',
               'the book <PP4E@learning-python.com>']
    try:
        import smtplib, email.utils, email.message         # email.* fails in Py 2.4
        sendserver = 'smtpout.secureserver.net'
        for player in players:
            msgobj = email.message.Message()
            msgobj['From']    = player
            msgobj['To']      = Signup
            msgobj['Subject'] = Subject
            msgobj['Date']    = email.utils.formatdate()
            msgobj.set_payload('Signing up for lotto...\n')

            print('Connecting...')
            rcpts = [Signup]
            if ccplayer: rcpts.append(player)
            server = smtplib.SMTP(sendserver)
            failed = server.sendmail(player, rcpts, str(msgobj))
            server.quit()
            assert not failed 
            print(str(msgobj))
    except: 
        pass  # smpt not supported here?  older 2.X email lib?

    # also add to names file for testing
    file = open(Filename, 'a')
    for player in players:
        file.write(player + '\n')
    file.close()

def resetFile(filename=Filename):
    open(filename, 'w').close()    # empty the players names file
    print('Players file cleared. ')

def resetEmails():
    print('Run main logic to clear emails, with [-find email -show S].')

def testLotto():
    """
    test all 4 main lotto show/find combos: console|cgi * email|file
    mixes methods from classes per modes just like runLotto() below; 
    this is essentially a class factory: makes new classes in loop;
    """
    for shower in ShowConsole, ShowCGI:
        for finder in FindFile, FindEmails:
            printN('*' * 80, shower, finder)
            sendTestPlayers()
            time.sleep(10) # a guess
            class PyLotto(shower, finder, Picker): pass
            PyLotto().run()
            resetFile()

def runLotto():
    """
    main logic: run the lottery in the show/find modes given 
    in script's cmdline args (default modes = email/console),
    mixing together selectable run mode classes plus Picker;
    """
    showModes = dict(console=ShowConsole, cgi=ShowCGI)
    findModes = dict(email=FindEmails, file=FindFile)
    config    = dict(show='console', find='email')        # [-show S] [-find F]
    for arg in config:
        try:
            config[arg] = sys.argv[sys.argv.index('-' + arg) + 1]    
        except:                                                      
            pass

    shower, finder = showModes[config['show']], findModes[config['find']]
    class PyLotto(shower, finder, Picker):
        pass
    PyLotto().run()         

def handleFormSubmit(filename=Filename):
    """
    the input form or URL's query parameters have already 
    been parsed here, so we can treat CGI inoputs as simple
    command-line arguments: see RunAsCGI logic in __main__;
    opens file for appending, with exclusive access lock to
    support concurrent updates in web mode (close unlocks);
    """
    if not os.path.exists(filename):
        open(filename, 'w').close()
    try:
        player = sys.argv[sys.argv.index('-form') + 1]    
        fd = os.open(filename, os.O_EXCL | os.O_APPEND | os.O_WRONLY)   
        line = (player + '\n').encode()                   
        os.write(fd, line)                  # 3.X: encode to bytes, no-op on 2.X
        os.close(fd)
    except:                                                      
        player = '...Error!\n%s\n%s' % sys.exc_info()[:2]

    if RunAsCGI:
        # assume run as a web server: html reply
        print('<HTML>')
        print('<TITLE>PyLotto</TITLE>')
        print('<BODY><H1>PyLotto Sign-up</H1>')
        print('<P>')
        print('Signed up: %s' % cgi.escape(player))       # oct11: escape this too!
        print('</P></BODY></HTML>')
    else:
        # may be run from console with -form cmdline arg
        print('Signed up: %s' % player)

def initAsCGI():
    """
    in CGI mode: translate URL query parameters to command-line arguments;
    cmdline args not passed through on my ISP when run remotely via URL;
    includes both switches as well as form input field for sign-ups;
    emit CGI reply hdr now too: may wrap console or html result display;
    """
    print('Content-type: text/html\n')         # emit reply header now
    sys.stderr = sys.stdout                    # display any Python errors

    urlparams = cgi.FieldStorage()             # parse, xlate params
    for key in urlparams.keys():
        sys.argv.extend([key, urlparams[key].value])

    #cgi.print_environ()
    #cgi.print_arguments()

if __name__ == '__main__':
    usage1 = 'pylotto.py [-send | -reset | -test | -form player | [-show S] [-find F] ]'
    usage2 = '(S = console | cgi, F = email | file, defaults: console, email)'

    # web: translate URL params, emit header
    if RunAsCGI:
        initAsCGI()  # changes sys.argv

    # run admin modes
    if '-send' in sys.argv:
        sendTestPlayers()               # send test emails/file lines
    elif '-reset' in sys.argv:
        resetFile()                     # clear state (as possible)
        resetEmails()
    elif '-test' in sys.argv:
        testLotto()                     # test all lotto mode combinations
    elif '-form' in sys.argv:
        handleFormSubmit()              # save submitted player in CGI mode 

    # run main logic
    elif '-show' in sys.argv or '-find' in sys.argv:
        runLotto()                      # run lotto with selected modes
    else:
        print('Usage:\n%s\n\t%s' % (usage1, usage2))