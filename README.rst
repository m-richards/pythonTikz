pythonTikZ |Integration| |Latest Docs|
======================================

  ..  ..|Travis| |License| |PyPi| |Stable Docs| |Latest Docs|

pythonTikZ is a Python library creating TikZ graphics in LaTeX.
The library began in concept as a fork of
`PyLaTeX <https://jeltef.github.io/PyLaTeX/current/>`_, which still
forms a basis for the package. Its goal is to provide a higher
level interface, less error prone interface to writing TikZ,
whilst still exposing enough low level detail that complex 
diagrams can be produced. Whilst most changes are in the form of additional
functionality, some of the PyLaTeX base classes have been modified for a
cleaner user experience.

The library aims to provide a convenient, reusable way
of writing TikZ where documentation and type hinting
are available to aid in this process.


Installation
------------
pythonTikZ works on Python 3.6+
Currently it also will work on earlier versions of Python 3, but this is not
a continuing commitment, use of f-strings are expected in future development.
PyLaTeX however does support a wider array of python versions, perhaps the
limited support of pythonTikz will be reviewed at a later date.

Currently one can install from the repository directly using pip::

   pip install git+https://github.com/m-richards/pythonTikz.git

Currently, the package is not PyPi, however this should change as the project
progresses.

Documentation
-------------

There currently is only one version of the docs, that is linked to the
current master branch. Once out of alpha, the intent is to maintain a link to
versions with an associated pypi release as well:

- The one generated for the `lastest git version
  <https://m-richards.github.io/pythonTikz/>`__.


Contributing
------------

Read the `How to
contribute <https://m-richards.github.io/pythonTikz/contributing.html>`__
page for tips and rules when you want to contribute.

Examples
--------
The documentation is slowly showing more pythontikz specific examples of
functionality. See `Examples <https://m-richards.github
.io/pythonTikz/examples.html>`__ to compare the python, generated tex, and
the output pdf.

The following picture shows raw PyLaTeX usage and does not demonstrate any of
the additional features of pythontikz.

.. figure:: https://raw.github.com/JelteF/PyLaTeX/master/docs/source/_static/screenshot.png
   :alt: Generated PDF by PyLaTeX

Copyright and License
---------------------
Copyright 2020 Matthew Richards,
Original copyright:
Copyright 2014 Jelte Fennema, under `the MIT
license <https://github.com/m-richards/pythonTikz/blob/master/LICENSE>`__

.. |Integration| image:: https://img.shields.io/circleci/build/github/m-richards/pythonTikz.svg?style=svg
    :target:https://circleci.com/gh/m-richards/pythonTikz
   

.. .. |PyPi| image:: https://img.shields.io/pypi/v/pylatex.svg
 ..   :target: https://pypi.python.org/pypi/PyLaTeX
   
.. |Latest Docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
     :target: https://m-richards.github.io/pythonTikz/
   
.. .. |Stable Docs| image:: https://img.shields.io/badge/docs-stable-brightgreen.svg?style=flat
 ..    :target: https://jeltef.github.io/PyLaTeX/current/
