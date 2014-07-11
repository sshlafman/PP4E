#!/usr/bin/python
"""
=====================================================================
PyLotto: select students of a class at random to receive copies
of a book;  I use this to give away a few free copies of Python
books in some of the classes I teach;  students enter the lottery
by sending an email message to "PP4E@learning-python.com", with 
subject "PYLOTTO", and their email address in the From header;  
winners are picked by scanning the email inbox and parsing emails
to find the entrants, and selecting from them at random;  

see Chapter 13 for much more on email tools, and Part 2 for hints
on adding a tkinter GUI for sign-up or reporting;  major caveat: 
this requires that POP email access be supported at the training
site, and this is not always the case in some closed contexts -- 
this may need to be run offsite, run on a remote server via telnet
or SSH (e.g., PuTTY), or invoked with a Web URL as a server-side 
CGI script that produces an HTML reply page;  the latter CGI option 
assumes your server runs Python 3.X as required by the current code
here, or you port this for use on Python 2.X servers (see asCgi() 
below for pointers, and see Chapter 15 for more on CGI in general);

update: now includes test mode that sends canned test emails, as
well as a cgi mode that prints the required headers and html tags;
could also send winners reply email, but SMTP is even less common;
alt: a CGI signup form and server-side dbase, but I prefer email;
also see pylotto24.py for a version that runs on Python 2.4 servers;
=====================================================================
"""

import poplib, email, random, getpass, pprint, sys

Drawings = 3
Signup   = 'PP4E@learning-python.com'
Subject  = 'PYLOTTO'
Server   = 'pop.secureserver.net'
RunAsCGI = False  # remote web URL?
 
def findPlayers(signup, subject, server, password, trace=print, hastop=True):
    """
    find and remove signup emails.
    py3.1 email requires decoding mail text to str (3.2 may not);
    messsage_from_string(s) == email.parser.Parser().parsestr(s);
    removes duplicate email addresses, but may not be sufficient;
    """
    players = []
    server = poplib.POP3(server)
    server.user(signup) 
    server.pass_(password)
    trace(server.getwelcome())
    trace(server.list())
    try:
        msgcount, msgbytes = server.stat()
        for i in range(msgcount):
            trace('message %s of %s...' % (i+1, msgcount))
            if not hastop:
                hdr, msgbytes, octets = server.retr(i+1)            # get full text
            else:
                hdr, msgbytes, octets = server.top(i+1, 0)          # headers only

            msglines = [line.decode('utf-8') for line in msgbytes]  # 3.1: to str
            msgtext  = '\n'.join(msglines)
            msgobj   = email.message_from_string(msgtext)           # parse text
            if msgobj['Subject'].upper() == subject:
                players.append(msgobj['From'])
                server.dele(i+1)                                    # del on quit
    finally: 
        server.quit()           # be sure to unlock mailbox on exit    
    return list(set(players))   # remove duplicate email addresses

def pickWinners(players, drawings):
    """
    choose winners at random.
    note: set.pop() is defined to remove an arbitrary set item 
    too, but I'd rather rely on the random module explicitly here
    to be sure that this is fair ("arbitrary" may be arbitrary);
    """
    winners = []
    for i in range(drawings):
        if not players:
            break
        else:
            drawn = random.choice(players)
            players.remove(drawn)
            winners.append(drawn)
    return winners

def main(password, trace=print):
    """
    main logic, modularized for reuse as cgi and tests
    """
    players  = findPlayers(Signup, Subject, Server, password, trace)
    print('Players:')
    pprint.pprint(players)

    winners  = pickWinners(players, Drawings)
    print('Winners:')
    pprint.pprint(winners)

def sendTestMails():
    """
    split off so callable during interactive testing
    """
    import smtplib, email.utils, email.message
    sendserver = 'smtpout.secureserver.net'
    players = ['"Book support" <lutz@rmi.net>',            # try various formats
               'lutz@learning-python.com',
               'the book <PP4E@learning-python.com>']

    for player in players:
        msgobj = email.message.Message()
        msgobj['From']    = player
        msgobj['To']      = Signup
        msgobj['Subject'] = Subject
        msgobj['Date']    = email.utils.formatdate()
        msgobj.set_payload('Signing up for lotto...\n')

        print('Connecting...')
        server = smtplib.SMTP(sendserver)
        failed = server.sendmail(player, [Signup, player], str(msgobj))       # cc player
        server.quit()
        assert not failed 
        print(str(msgobj))

def asTest(password):
    """
    send a few test mails prior to main logic;
    give emails time to show up before main();
    """
    import time
    global Drawings
    Drawings = 1
    sendTestMails()
    print('[pausing...]')
    time.sleep(20)         # just a guess, really
    main(password)

def asCgi(password):
    """
    run main logic on web server in response to client, to be
    sure POP mail will be usable; prints HTML to create reply;
    invoke url=http://www.py3xservername.com/cgi-bin/pylotto.py,
    from a web page (html) or using Python's urllib in a script;
    this assumes that the browser won't time-out before reply;
    to do: wrap print so all text is run though cgi.escape()?;
    to do: convert print/unicode usage so this runs on 2.X servers?
    done => see pylotto24.py for a port that runs on Python 2.4;
    """
    print('Content-type: text/html\n')
    print('<HTML>')
    print('<TITLE>PyLotto</TITLE>')
    print('<BODY><H1>PyLotto Results</H1>')
    print('<P><PRE>')
    main(password, trace=lambda *kargs, **pargs: None)
    print('</PRE></P></BODY></HTML>')

if __name__ == '__main__':
    if RunAsCGI:
        # run on web server; add pswd security here
        password = open('pylotto.pswd').readline().rstrip()
        asCgi(password)
    else:
        # run in console, on client or remote server
        password = getpass.getpass('pop email password?')
        if len(sys.argv) > 1:
            asTest(password)
        else:
            main(password)             
