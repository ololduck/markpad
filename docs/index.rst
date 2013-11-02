.. Markpad documentation master file, created by
   sphinx-quickstart on Sat Nov  2 15:38:34 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Markpad's documentation!
===================================

.. toctree::
   :maxdepth: 2



Why?
--------

We had a lot of reports to write, and sometimes, we had to do it with other students. So we needed a collaborative editor. Also, we had to send PDF files, the prettiest and easiest to read. Markdown allows this, and the learning curve is much smaller than ReStructuredText.

I have searched the web for this kind of projects, but each time, either the collaborative editing or the pdf render was lacking. So I decided to build my own.


How?
--------

With my hands.

Jokes apart, markpad was written in python. It uses the flask web framework to handle the server part, sql-alchemy for the data models, and the standard markdown python lib for the conversion. A bit of AJAX is also at hand.


May I contribute?
-----------------

Of course. The server part is near-finished. A bit of a redesign is needed, not only in UI terms but also UX.

The main repository is at github_. You can fork it and submit a pull request. You can also contact me.



.. _github: https://github.com/paulollivier/markpad


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

