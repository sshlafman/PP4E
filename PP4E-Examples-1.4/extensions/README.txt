***UPDATE OCTOBER 2013: see Pillow's description im the PIL README file here*** 

**UPDATE JULY 2012: see also PIL-for-3.2-and-3.3-README.txt in this directory.**

*The PIL here was a prerelease version: see the web for an official 3.X release*

This directory contains the PIL image-processing extension used by
some of the book's GUI examples.  Run this file to install PIL's
files on your machine, and unpack the zip file here in the Python
site-packages directory (or manually copy its contents into PIL's 
install source tree; it contains patches needed while the port
was being developed--replacement files for standard PIL).

This PIL is a very early release for Python 3.1 on Windows.  Be
sure to search the web for newer versions of PIL, as well as PIL 
for other platforms.  

If you cannot install PIL, many of the PIL-based GUI examples will 
work anyhow if you comment-out their PIL import statements, but they 
will be limited to Tk's image type support (GIFs and bitmap formats),
and the PyPhoto example won't be able to do thumbnails or resizes.