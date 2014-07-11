#!python3
"""
-------------------------------------------------------------------------------
Try to guess the mood of the stock market by screen scraping
a financial news site for positive and negative terms.  This
reflects shifting human mood, not actual stock market values.

*This is a work in progress*: expand the search term patterns here.
Uses simplistic eliza-like heuristic, not a full html parse (this
is mostly just re pattern matching + urllib web page fetches).
Assumes .\audiofiles (mp3s which you must provide and list here)
and .\testfiles (tests) subdirs in this script's directory.

Drag this file out to a desktop shortcut to launch by icon clicks
on Windows (and similar elsewhere); it prints substantial trace
information to the console, including patterns and their matches.
-------------------------------------------------------------------------------
"""

import webbrowser, os, sys, re, pprint
from urllib.request import urlopen
trace = print

# future possibility?: full html parse
# from html.parser import HTMLParser


# Audio files------------------------------------------------------------------
# configure me: assumed to be in .\audiofiles
goodtune = "Everything's Coming Up Roses.mp3"
badtune  = 'Always Look On the Bright Side of.mp3'
mehtune  = "Lithium.mp3"


# Patterns---------------------------------------------------------------------
# grow me: accepts full re patterns or literal substrings, case is ignored;
# list variations individually or via '|' pattern: 'wall (?:street|st) rises';
# now computes terms auto: combines each noun with one of the verbs columns;


nouns = ['wall street',                      # terms = noun + ' ' + verb
         'wall st',                          # or 'wall (?:street|st)'
         'stocks',
         'markets',
         'market',
         's&p',
         's&p 500',
         'dow'
	] 


verbs = [('rises',      'falls'),             # (good, bad)
         ('rose',       'fell'),          
         ('rise',       'fall'),

         # '...s?' = optional trailing 's' [dow gains, stocks gain]
         # '?' applies to preceding pattern item: one char only

         ('gains?',     'loses?'),        
         ('expands?',   'contracts?'),
         ('grows?',     'shrinks?'),
         ('inflates?',  'declines?'),
         ('advances?',  'retreats?'),

         # 1st matches 'noun (opional-named-verb )up' [dow up, dow edges down]
         # 2nd matches an optional ('end '|'ends ') in middle [markets end higher]
         # 3rd matches a required  ('close '|'closes ') in middle [s&p closes lower]

    #    ('(?:(?:edges|closes) )?up',  '(?:(?:edges|closes) )?down'),
    #    ('(?:end(?:s)? )?higher',     '(?:end(?:s)? )?lower'),
    #    ('(?:close|closes) higher',   '(?:close|closes) lower'),

         # catchall, supercedes prior 3 patterns (don't count twice!):
         # matches optional 'any-alpha-string ' in middle [dow drifts higher, etc.]
 
         ('(?:[a-zA-Z]+ )?(?:up|higher)', '(?:[a-zA-Z]+ )?(?:down|lower)')
	]


goodterms = [(noun + ' ' + good) for noun in nouns for (good, bad) in verbs]
badterms  = [(noun + ' ' + bad)  for noun in nouns for (good, bad) in verbs]


# Fixup------------------------------------------------------------------------
# 'x rise' is a prefix of 'x rises' => count for first term only!
# can't assume true of both good and bad in original verbs tuple;
# ok for literals, but this may not be appropriate for some patterns?
trace('good=>\n', pprint.pformat(goodterms),end='\n\n')

goodterms = [term for term in goodterms if not
                  [other for other in goodterms
                             if other != term and term.startswith(other)]]

badterms  = [term for term in badterms if not
                  [other for other in badterms
                             if other != term and term.startswith(other)]]

trace('good=>\n', pprint.pformat(goodterms),end='\n\n')
trace('bad =>\n', pprint.pformat(badterms), end='\n\n')


# Main logic-------------------------------------------------------------------

# canned test files via cmd line arg, in .\testfiles
testpages  = ['test-good.htm', 'test-bad.htm', 'test-meh.htm']    # good=Fidelity.com
testpages += ['test-bad-pattern.htm', 'test-bad2.htm']            # re patterns, etc
testpages  = ['testfiles' + os.sep + test for test in testpages]

# configure me: live news page to scrape
newssite   = 'http://news.fidelity.com/news/topnews.jhtml'

# mode via command line arg (or not)
if len(sys.argv) > 1:
    test = testpages[int(sys.argv[1])]
    page = open(test, 'rb').read()               # pystockmood.py (0..4)?
    trace('opened:', test)
else:
    page = urlopen(newssite).read()              # else fetch live from web
    trace('fetched:', newssite)                  # this is also clicked case

# score the page, pick a tune
net = 0
for (kind, score, terms) in [('good', +1, goodterms), ('bad', -1, badterms)]:
    for term in terms:
        matches = re.findall(term.encode('utf8'), page, re.IGNORECASE)
        count = len(matches)
        if count:
            trace('...%d: %r -> %s' % (count, term, pprint.pformat(matches)))
        net += score * count
    trace(kind, '~', '%+d' % net)

tune = goodtune if net > 0 else (badtune if net < 0 else mehtune)
trace(net, '=>', tune)

# play the tune file
if sys.platform.startswith('win'):
    os.startfile('audiofiles\\' + tune)  # same as webbrowser on windows
    input('[Press Enter to close]')
else:
    webbrowser.open_new('file://%s/audiofiles/%s' % (os.getcwd(), tune))
