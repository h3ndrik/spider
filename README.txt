===========
mediaspider
===========

Multimedia-file crawler and webfrontend

Description
===========
Spider helps you to index, search and access your videos, audio-files and other files on your server. It consists of a filesystem crawler and a web-frontend.

Quickstart
==========
* python3 crawler --help
* python3 webui.py

Dependencies
============
* python3
* python3-sqlalchemy
* python3-argparse
* python3-bottle
(tested on GNU/Linux)

License
=======
Third party licenses:
* Regexs for tv_show filename parsing were borrowed from tvnamer (github.com/dbr/tvnamer) which is licensed public domain/unlicense
* Web-UI uses the Twitter Bootstrap framework (twitter.github.io/bootstrap/)
*        jQuery (jquery.com)
*        and mime-icons from the gnome project (gnome.org)
Spider itself is:
  :copyleft: 2013 by h3ndrik.
  :license: WTFPL, see LICENSE for more details.
