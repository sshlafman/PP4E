#!/usr/bin/python
"""
=====================================================================
Revisions labeled with "# XX", to run on a Python 2.4 web server
(godaddy.com's latest, as of Jan 2011);  runs in CGI mode by default, 
avoids 3.X Unicode decoding step, and uses print statements in Python 
2.4 where the "from __future__ import print_function" is not yet
available (in 2.6, this would enable the 3.X print function/name);

note that a "print(X)" works just like "print X" in Python 2.X,
and Python 2.4 has str + unicode and does not recognize bytes b'':
decoding to Unicode for 3.X here causes the 2.4 email parse to fail;
run in browser or via urllib at this URL (defaults to 1 winner, and
requires a pop password file to be present on the web server): 

    http://learning-python.com/cgi/pylotto24.py

See file pylotto.py for the original/main docstring removed here;
=====================================================================
"""

def _print(args): print args  # assume just one            # XX
import poplib, email, random, getpass, pprint, sys

Drawings = 1
Signup   = 'PP4E@learning-python.com'
Subject  = 'PYLOTTO'
Server   = 'pop.secureserver.net'
RunAsCGI = True  # remote web URL?                         # XX
 
def findPlayers(signup, subject, server, password, trace=_print, hastop=True):  # XX
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

  # XX      msglines = [line.decode('utf-8') for line in msgbytes]  # 3.1: to str
            msglines = msgbytes                                     # 2.4: str, no b'' 
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

def main(password, trace=_print):                                         # XX
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
    for player in ('lutz@rmi.net', 'lutz@learning-python.com'):
        msgobj = email.message.Message()
        msgobj['From']    = player
        msgobj['To']      = Signup
        msgobj['Subject'] = Subject
        msgobj['Date']    = email.utils.formatdate()
        msgobj.set_payload('Signing up for lotto...\n')

        print('Connecting...')
        server = smtplib.SMTP(sendserver)
        failed = server.sendmail(player, [Signup, player], str(msgobj))
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
    to do: convert print usage so this runs on 2.X servers too?
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