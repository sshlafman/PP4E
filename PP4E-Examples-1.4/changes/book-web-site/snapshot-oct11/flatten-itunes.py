"""
flatten Itunes subfolder tree contents to store on
a usb drive, for copying onto my Jeep's harddrive;
endwith() now allows tuple of strings to try, so we
don't need any(filelower.endswith(x) for x in seq);
"""

import os, pprint

flattenDir = r'D:\MarksItunes'
itunesRoot = r'C:\Users\mark\Stuff\Itunes'
playables  = ('.mp3', '.m4a')
protected  = ('.m4p',)
irrelevent = ('.jpg', '.ini', '.xml')

actions = dict(keep=[], skip=[], miss=[])
if not os.path.exists(flattenDir):
    os.mkdir(flattenDir)

for (dirHere, subsHere, filesHere) in os.walk(itunesRoot):
    for file in filesHere:
        filelower = file.lower()
        if filelower.endswith(playables):
            actions['keep'].append(file)
            cpfrom = os.path.join(dirHere, file)
            cpto   = os.path.join(flattenDir, file)
            open(cpto, 'wb').write( open(cpfrom, 'rb').read() )
        elif filelower.endswith(protected):
            actions['skip'].append(file)
        elif not filelower.endswith(irrelevent):
            actions['miss'].append(file)

pprint.pprint(actions)
for key in 'keep', 'skip', 'miss':
    print('Total %s: %s' % (key, len(actions[key])))
