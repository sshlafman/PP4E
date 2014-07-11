#!/usr/bin/python
"""
Move all image (and other) files in a directory tree into
a flat directory, adding date-taken (or file-mod-date) to
front of filename to make them unique and sortable by date.
Also adds numeric suffix to filename for duplicates, and
stores non-image files (e.g., movies) in separate flat dir.

Used to merge contents of multiple camera cards holding
photos and movies shot on multiple cameras over many years.
Place all your dirs and images in workdir\SOURCE and run
tagpix in its home directory, where workdir exists; creates 
both workdir\photos-bydate and workdir\movies-etc-bydate.

Requires PIL (or its newer Pillow fork which fully supports
3.X); the exif.py alternative seemed to fail for more files.
"""
from __future__ import print_function
import os, pprint, datetime, time
from PIL import Image
from PIL.ExifTags import TAGS
#import EXIF

workdir = 'tagpixmerged'
sourcedir    = os.path.join(workdir, 'SOURCE')
flatphotodir = os.path.join(workdir, "photos-bydate")
flatotherdir = os.path.join(workdir, "movies-etc-bydate")   # photos-unknown dropped

def configdirs():
    # make or empty to-dirs
    for subdir in (flatphotodir, flatotherdir):     
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        else:
            for tempname in os.listdir(subdir):
                os.remove(os.path.join(subdir, tempname))

def get_exif(fn):
    # get image metadata dict: copied PIL code + added try
    ret = {}
    try:
        i = Image.open(fn)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    except Exception as E:
        print('****', E, fn)
    return ret

def filemoddate(filepath):
    # get file mod date string, or a default
    try:
        filemodtime = os.path.getmtime(filepath)
        filemoddate = str(datetime.date.fromtimestamp(filemodtime))    # 'yyyy-mm-dd'
    except:
        filemoddate = 'unknown'                                        # sort together
       #filemoddate = str(datetime.date.fromtimestamp(time.time()))    # or use today?
    return filemoddate

def classify(sourcedir):
    photos, others = [], []
    for (dirpath, subshere, fileshere) in os.walk(sourcedir):
        for filename in fileshere:
            filepath = os.path.join(dirpath, filename)
            pictags  = get_exif(filepath)
            if not pictags:
                # no exif metadata found: use file date
                moddate = filemoddate(filepath)                    # try file moddate 
                if filename[-4:].lower() in ['.jpg', '.jpeg']:     # photo (or mimetype)
                    photos.append((moddate, filename, filepath))
                else:
                    others.append((moddate, filename, filepath))   # movies, etc.
            else:
                # recognized images: try tags first, then file date
                fulltaken = ''
                for trythis in ('DateTimeOriginal', 'DateTimeDigitized'):
                    try:
                        fulltaken = pictags[trythis]               # normal: use 1st
                    except KeyError:                               # tag may be absent
                        pass
                    if fulltaken.strip():                          # bursts: 1st='  '
                        break
                splittaken = fulltaken.split()                     # fmt='date time'
                datetaken  = splittaken[0] if splittaken else ''
                if datetaken:
                    datetaken = datetaken.replace(':', '-')        # [0]='yyyy:mm:dd'
                    photos.append((datetaken, filename, filepath))
                else:    
                    moddate = filemoddate(filepath)                # mod='yyyd-mm-dd'
                    photos.append((moddate, filename, filepath))
    return photos, others

def moveone(filename, filepath, flatdir, kind, ix):
   #mover = lambda x, y: None
    mover = os.rename
    if os.path.exists(os.path.join(flatdir, filename)):
        print('****duplicate', kind, filename)
        front, ext = os.path.splitext(filename)
        filename = '%s__%s%s' % (front, ix, ext)    # add unique id suffix before ext
    flatpath = os.path.join(flatdir, filename)
    print(filepath, '=>', flatpath)
    mover(filepath, flatpath)

def moveall(photos, others): 
    for (ix, (datetaken, filename, filepath)) in enumerate(photos):
        filename = '%s__%s' % (datetaken, filename)                      # date prefix
        moveone(filename, filepath, flatphotodir, 'photo', ix)
    print('-'*80)
    for (ix, (datetaken, filename, filepath)) in enumerate(others):
        filename = '%s__%s' % (datetaken, filename)                      # date prefix
        moveone(filename, filepath, flatotherdir, 'other', ix)
    print('-'*80)
    """
    for (ix, (filename, filepath)) in enumerate(bads):                   # dropped alt
        filename = '%s__%s' % (filepath.split(os.sep)[-2], filename)     # dir prefix
        moveone(filename, filepath, flatbaddir, 'bad', ix)
    """
    
def unmoved(sourcedir):
    missed = []
    for (dirpath, subshere, fileshere) in os.walk(sourcedir):            # skipped?
        for filename in fileshere:
            missed.append(os.path.join(dirpath, filename))
    print('Missed:', len(missed))
    pprint.pprint(missed)

configdirs()
photos, others = classify(sourcedir)
print('photos, others:', len(photos), len(others))
pprint.pprint(photos); print('-'*80)
pprint.pprint(others); print('-'*80)
moveall(photos, others)
unmoved(sourcedir)
print('Bye.')

