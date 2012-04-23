Introduction
============

"dmenu-do" is a thin wrapper around dmenu which makes it act a little more like
gnome-do.  Specifically, it allows the user to traverse a set of directories and
find files stored in them.  It then either executes the file, or uses mailcap to
run an associated program.


Installation
============

To run this you should install Python (duh) and you should install and configure
mailcap.  You should also edit the DMENU constant at the top of the "dmenu-do"
source file to change how dmenu is called and control font, colors, etc.  You
should also edit the FOLDERS constant and put in your own set of folders to
search.

Usage
=====

Once you run dmenu-do, you will get a list of all executables from your PATH,
and the list of FOLDERS.  If you hit ENTER on an executable (e.g. "firefox" or
"emacs"), it will just execute.  If you hit ENTER on a directory, dmenu will
display the items (files and folders) within that directory.  If you hit ENTER
on a directory again, items in that directory will show, etc.  If you hit ENTER
on a file that is not an executable, dmenu-do will call mailcap's "see" on the
file, and whatever program you have configure to run it will be launched.

TODO
====

Sort items in MRU order.


License
=======

Copyright (C) 2012 Eyal Erez

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA.
