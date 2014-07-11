"""
rename files dropping numeric digits at front (track/disc 
numbers, like "02 xxx.mp3", "02 - xxx.mp3", "3-02 xxx.mp3");
these make it difficult to sort to detect duplicates, etc.;
after N-dir merge via drag-and-drop;  3.X-only: input();
"""

import os, string

cwd = input('Directory to scan?')
os.chdir(cwd)
for name in os.listdir('.'):
    if not os.path.isfile(name):                      # skip subdirs, "."?
        continue
    if name[0] in string.ascii_letters:               # skip if alpha start already
        continue
    print()
    if input('Rename? "%s"' % name).lower() != 'y':   # valid: "2112 Overture.mp3"
        print('skipped')
        continue

    rename = name
    while rename and rename[0] not in string.ascii_letters:   # scan to first alpha
        rename = rename[1:]
    altname = input('new name? ["%s"]' % rename)              # Enter=[suggestion]
    if altname: rename = altname

    if os.path.exists(rename):
        print('DUPLICATE SKIPPED: "%s" -> "%s"' % (name, rename))
    else: 
        os.rename(name, rename)
        print('renamed: "%s" -> "%s"' % (name, rename))



"""
-----------------------------------------------------------------------------------
Example run:

E:\Music\resolve-itunes-nov11>renamer.py
Directory to scan?C:\MusicMergeNov11

Rename? "(What's So Funny 'Bout) Peace, Love.mp3"
skipped

Rename? "01 - Four Wheel Drive.mp3"y
new name? ["Four Wheel Drive.mp3"]
renamed: "01 - Four Wheel Drive.mp3" -> "Four Wheel Drive.mp3"

Rename? "01 - She Drives Me Crazy.mp3"y
new name? ["She Drives Me Crazy.mp3"]Hmmm.mp3
renamed: "01 - She Drives Me Crazy.mp3" -> "Hmmm.mp3"

Rename? "01 Always Look On the Bright Side of.m4a"
skipped

...
"""