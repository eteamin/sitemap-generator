sitemap-generator
=================

Documentation
-------------
Simple multi-thread sitemap generator in python


Depends on
----------
requests


Usage
-----

Simply:

.. code-block:: bash

  python main.py --url http://github.com --timeout 3 --path /path/to/final/destination

In case you don't provide path, a folder named output will be created in the current working directory
and the sitemaps will be generated inside it.
