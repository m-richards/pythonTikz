How to contribute
=================

.. highlight:: bash

First of all, if anything is incorrect or something is missing on this page (or
any other for that matter), please send in a pull request. It is important that
setting up the development environment is as painless as possible.

Setting up the development environment
--------------------------------------
It is **strongly** recommended to have a Linux environment set up
in the development process to run the integration tests from. They are written
in bash and so mileage may vary on other operating systems.

This does not however mean that all development needs to take place on a
Linux OS. I develop on windows and use WSL to run the integration tests.

Regardless of operating system, you will however need a LaTeX distribution
(obviously) so that pdflatex or latexmk can be run.

Note that TeXLive need not be used, MikTeX or other LaTeX distributions should
work fine (I build with pdflatex using MikTeX on windows, but TeXLive on WSL)


Linux dependencies
~~~~~~~~~~~~~~~~~~

For Ubuntu and other Debian based systems::

    sudo apt-get install python3 python3-dev virtualenv \
        texlive-pictures texlive-science texlive-latex-extra \
        imagemagick


Getting the source code
~~~~~~~~~~~~~~~~~~~~~~~
You need your own fork of the `Github repository
<https://github.com/m-richards/pythonTikz>`_ by using the Github fork button. You will
then need to clone your version of the repo using the normal way, something
like this::

    git clone https://github.com/YourUserName/pythonTikz
    cd pythontikz
	
It is also fairly likely you will need a fork of the parent library
`<https://github.com/JelteF/PyLaTeX>`_ if you need to modify any of the
underlying base classes (you can download a local copy in the same -
see its own contributing documentation for details).  pythonTikz
is designed to operate as a wrapper sitting on top of this library to reduce
maintenance and avoid duplication of code.

This doesn't however mean that you should make changes and submit pull
requests to PyLaTeX (unless of course your changes are more general than
pythonTikz, in which case you should probably be contributing there).
Instead, make your changes in your local pythontikz fork and adjust
the inheritance chain accordingly.

Make your own branch for your specific feature or fix (don't do this just on
master)::

    git checkout -b your-nice-feature


Python environment setup
~~~~~~~~~~~~~~~~~~~~~~~~
This method will use a virtual environment, this is the easiest way to get all
the dependencies.

1. Create a virtualenv by running::

    virtualenv venv -p python3

2. Activate it by running (you should do this whenever you start working on
   your changes)::

    source venv/bin/activate

3. Install all the development dependencies inside the virtual environment by
   running::

    pip install -r dev_requirements.txt


Some tips before starting
-------------------------
1. Make sure your install hasn't broken anything before you start. You should
   be able to run ``testall.sh`` with no issues before you get started on your
   changes
2. Look at the code that is already there when creating something new, and
   also make sure it isn't part of
   `PyLaTeX <https://jeltef.github.io/PyLaTeX/current/>`_.
3. To learn how to squash commits, read this `blog
   <http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html>`_.
   Ignore the word of caution (saying that interactive rebases after changes
   are pushed are bad), since this is directed to the case that other people
   are working on the branch that your force push will override.

   You can do this when you have a couple of
   commits that could be merged together. This mostly happens when you have
   commits that fix a typo or bug you made in a pull request and you fix that
   in a new commit.

Some rules
----------
There are two things that are needed for every pull request:

1. Run the ``testall.sh`` script before making a pull request to check if you
   didn't break anything.
2. Follow the **PEP8** style guide and make sure it passes pyflakes (this is
   also tested with the ``testall.sh`` script).
3. Have a look at the coverage results locally before pushing your PR. This
   is really easy to do and shows quite clearly whether your new changes
   leave holes in what the testt cover. From the base directory::

    coverage run --source=pythontikz -m pytest -v tests/*
    coverage report
    coverage html

   This generates a nice easy to read breakdown of the coverage in ``htmlcov/``
   . Start by looking at ``index.html``.

These are also tested for by Travis, but please test them yourself as well.

Depending on your type of changes some other things are needed as well.

1. If you add new arguments, function or classes, add them to
   ``tests/args.py`` without forgetting to name the arguments. That way it is
   easy to see when the external API is changed in the future.
2. Change docstrings when necessary. For instance when adding new arguments or
   changing behaviour.
3. If you fix something, add a **test** so it won't break again.
4. If you add new functionality add **tests** for it. Make sure that the
   code actually does what you think it does! Also make sure that it breaks
   when you expect it to break. It is far more user friendly if you can catch
   formatting errors in the python, rather than waiting for the latex
   compilation to fail.
5. If your change is user facing, add it to the **changelog** so it will be
   mentioned in the next release. Its location is at
   ``docs/source/changelog.rst``.
6. If you add something new, show it off with an **example**. If you don't do
   this, I will probably still merge your pull request, but it is always nice
   to have examples of features.
