.. pythonTikZ documentation master file, created by
   sphinx-quickstart on Sun Jan 26 21:11:24 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pythonTikZ - `(Github repository) <https://github.com/m-richards/pythonTikz>`_
==============================================================================
pythonTikZ is a Python library creating TikZ graphics in LaTeX. 
The library began in concept as a fork of PyLaTeX, which still
forms a basis for the package. Its goal is to provide a higher
level interface, less error prone interface to writing TikZ,
whilst still exposing enough low level detail that complex 
diagrams can be produced.

**pythonTikZ is not a substitute for learning TikZ (unfortunately).**
However, the intent is to make available a number of easy to use wrappers,
which hide the TikZ writing details beneath a relatively intuitive exterior.
The hope is that pythonTikZ eases the burden of using TikZ for occasional
TikZ users, making image production a simple iterative process, without the
need to continually look up "how do I do xyz in TikZ?"

The library aims to provide a convenient, reusable way
of writing TikZ where documentation and type hinting
are available to aid in this process. The intention is that the python
interface is easy to understand at a glance and thereby is easily modified
and more reusable.

It does not promise concise output TikZ. Whilst one could use
the various TikZ styles to write less verbose TikZ, this has a nontrivial
implementation burden. Additionally, it introduces the need to heuristically
determine when a style definition is "worthwhile".

Finally, pythontikz aims to be more strict about the testing of new function
than PyLaTeX (currently) is. Unit tests should verify that the output is as
expected (which in turn should be valid TikZ).

Installation
------------
pythonTikZ works on Python 3.6+
To be completed

Support
-------
This library is developed for use on Windows, but is tested on WSL. 
This should mean the library will work on both platforms but there is
potential for some cases where they do not.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   usage
   examples
   api
   changelog
   contributing



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
