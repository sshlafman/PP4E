This is the examples distribution package for the book
_Programming Python, 4th Edition_, published in January 2011.

The "PP4E" directory here is a Python package root, containing 
all the example files found in the book.  Paths in this tree 
correspond to the book's example labels and system prompts.

See the "__init__.py" file at the top level of the PP4E
directory here for addition usage information.  In short:

--You can run many of its examples with the auto-launcher 
  scripts located at the top level of the PP4E directory.
  See the book and file "PP4E\README-PP4E.txt" here (a more 
  verbose guide for novices) for details on these scripts.

--To import the package's code in other programs, and to run
  some examples inside it without the auto-launchers, copy the 
  PP4E directory here to a directory on your computer's file 
  system, and add the directory immediately above PP4E (i.e.,
  its container on your machine) to your PYTHONPATH setting.

Most intra-package imports in book examples are fully-specified
package imports relative to this PP4E root, not package-relative;
their imports do not depend on their location, and their module 
names will not clash with other code.  A few same-package imports
use package-relative syntax, but package clients aren't affected.

If you've obtained this package on a write-only medium such 
as a CD, you can still make use of its code directly in both
ways above, but copying it to a writeable directory allows you
to make changes, and allows Python to save bytecode for quicker 
program start-ups.

For updates, watch http://www.rmi.net/~lutz/about-pp4e.html, or
http://learning-python.com/books.  To post errata found, please 
see O'Reilly's page for this book. 

--Mark Lutz, July 2010 (updated October 2013)