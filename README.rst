******************************
Dot - Simple Dotfiles Tracking
******************************

.. image:: https://circleci.com/gh/erroneousboat/dot.svg?style=shield
    :target: https://circleci.com/gh/erroneousboat/dot

Beta
====
Take note that this project is still in its infancy and is, at the moment, mainly as a personal project. If you want to know when the project receives updates than give it a star or watch.

Manual
======

Installation
------------
Download the tar.gz file from the dist folder and install it with the following
command:

    $ pip install dot-<version-number>.tar.gz

Setting up
----------
First create a folder in which you want to put all the files and folders in.
In this directory all the tracked files will reside. For instance create a
dotfiles folder in your home directory.

    $ mkdir ~/dotfiles

Go to this directory and execute the  ``dot init`` command. This command will 
create a backup folder and a files folder. The files folder will contain all
the files and folder you are going to track and the backup folder will contain
the files and folders that will backup when you are using 'dot' on a different
machine.

Now that you've created the basic structure, be sure to set up a git repository
for this folder. Go to your dotfiles directory an execute the following
command.

    $ git init

For further instructions on how to set up a git repository refer to the git
documentation.

Tracking files/folders
----------------------
To track a file or folder simply use the following command:

    $ dot add <name> <path>

Specify the name you'd like to setup for this symlink and the path which leads
to the file or folder you want to track. For instance:

    > dot add dottestfile ~/.dottestfile

When that succeeds you can symlink the tracked file by using the command 
``dot``.

    $ dot

This will transfer the tracked files and folders to the files directory in your
dotfiles folder.

Deleting
--------
If you want to reset the link you just made, then type in the following command:

    $ dot rm <name>

Use the name you described when adding the file, you can reference this name by
typing 'dot list', this will give you an overview of the files that are being
tracked.

    $ dot rm dottestfile

This will return the file to its original destination and won't be tracked in
the future. Just make sure you made the necessary changes in git.

Help
----
When you're stumped at what command to use than use:
    
    $ dot --help

This will display the available command and how to use it.

Other machines
--------------
So you have setup your repository and are tracking your dotfiles but you want 
to be able to use your repository with your updated file on another machine.
Then first we'll track dot's own dotfile: '.dotconfig'.

    $ dot add dotconfig ~/.dotconfig
    
    $ dot

This file contains all the locations and files you are tracking on the moment.
Make the necessary changes to your git repository and clone it on the other
machine. Now run the command ``dot`` and it will begin symlinking the files that
are stored in the .dotconfig file. When files are missing the program will let
you know.

Feedback / Contact
==================
If you uncovered an issue or bug then let me know or file an issue on the
github page. If you want to give some feedback or have a question then you can
contact me on this e-mail address: erroneousboat@gmail.com

Contributing
============
If you want to help with the development of this application then please refer
to the CONTRIBUTING.rst to get started.