******************
Dot - Contributing
******************

Introduction
============
If you want to help with the development of this application then that would be
awesome! Fork the repo, hack on it and make a pull-request. In order to get you
started with developing, take the following steps:

Setup
=====
1. First clone this repository
    $ git clone <repo>

2. Install virtualenv on your system
    $ pip install virtualenv

3. To setup a `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ for dot, execute the following command in the dot folder
    $ virtualenv env

4. To activate virtualenv, use this command:
    $ source env/bin/activate

5. Now install the development packages that you need, with the following command:
    $ pip install -r dev_requirements.txt

6. And when you want to test out the program: 
    $ python setup.py develop

Testing
=======
Installing the dependencies will also install nosetests. To execute the test
runner, just type in this command:
    $ nosetests

If you want the check the code coverage of the module, then do that with the 
following:
    $ nosetests --with-coverage --cover-erase

When you're done
================

When you done hacking around, type the following:
    $ python setup.py develop --uninstall