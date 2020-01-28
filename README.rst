pythonTikZ
====================

  ..  ..|Travis| |License| |PyPi| |Stable Docs| |Latest Docs|

This repository is still experiencing migratory changes as it departs
from being a fork of PyLaTeX and becomes a package extension to
PyLaTeX as a standalone package. Please keep this in mind,
as some links and text still refer to the original repository.
Additionally, duplicated code sections will be progressively
removed from this repository.

pythonTikZ is a Python library creating TikZ graphics in LaTeX. 
The library began in concept as a fork of
`PyLaTeX <https://jeltef.github.io/PyLaTeX/current/>`_, which still
forms a basis for the package. Its goal is to provide a higher
level interface, less error prone interface to writing TikZ,
whilst still exposing enough low level detail that complex 
diagrams can be produced. 

The library aims to provide a convenient, reusable way
of writing TikZ where documentation and type hinting
are available to aid in this process.


Installation
------------
Fork the Repository
 .. Simply install using ``pip``::

 ..    pip install pylatex

Documentation
-------------

There are two versions of the documentation:

- The one generated for the `last stable release
  <https://jeltef.github.io/PyLaTeX/current/>`__.
- The one based on the `latest git version
  <https://jeltef.github.io/PyLaTeX/latest/>`__.

Contributing
------------

Read the `How to
contribute <https://jeltef.github.io/PyLaTeX/latest/contributing.html>`__
page for tips and rules when you want to contribute.

Examples
--------
.. todo:: Update this
The documentation contains a lot of examples that show the
functionality. To give an impression of what can be generated see this
picture:

.. figure:: https://raw.github.com/JelteF/PyLaTeX/master/docs/source/_static/screenshot.png
   :alt: Generated PDF by PyLaTeX

Copyright and License
---------------------
Copyright 2020 Matthew Richards,
Original copyright:
Copyright 2014 Jelte Fennema, under `the MIT
license <https://github.com/m-richards/pythonTikz/blob/master/LICENSE>`__

.. .. |Travis| image:: https://img.shields.io/travis/JelteF/PyLaTeX.svg
 ..   :target: https://travis-ci.org/JelteF/PyLaTeX
   
 .. .. |License| image:: https://img.shields.io/github/license/jeltef/pylatex
.svg
   :target: https://img.shields.io/github/license/m-richards/pythontikz.svg

.. .. |PyPi| image:: https://img.shields.io/pypi/v/pylatex.svg
 ..   :target: https://pypi.python.org/pypi/PyLaTeX
   
.. .. |Latest Docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
     :target: https://jeltef.github.io/PyLaTeX/latest/
   
.. .. |Stable Docs| image:: https://img.shields.io/badge/docs-stable-brightgreen.svg?style=flat
 ..    :target: https://jeltef.github.io/PyLaTeX/current/
