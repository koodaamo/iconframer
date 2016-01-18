===============================
Iconframer
===============================

.. image:: https://badge.fury.io/py/iconframer.png
    :target: http://badge.fury.io/py/iconframer


Generate framed, labeled SVG icons.

Features
--------

* Frame SVG icons using a template and apply a label (localized via gettext)
* Optionally, convert to PNG (requires pycairo/cairocffi & python-rsvg)
* Optionally, inverse the icon (assumes icon is black & white only)


How to use
-----------

Create SVG file with one layer per icon. Create another SVG to use as the frame template.
Then configure the settings (see config example at docs/iconframer.yaml) and run the
'iconframer' command line to generate icons:

::
  Usage:

   iconframer (svg | pdf | png) <language> ... [--config=<file>] [--size=<size>] [--nolabel] [--inverse] [--translations=<path>]
   iconframer -h | --help
   iconframer --version

  Options:

   -i --inverse                     Inverse the icon colors
   -n --nolabel                     Do not generate labeling
   -t <path> --translations=<path>  Specify path of i18n file (locale) structure, by default 'i18n'
   -s <size> --size=<size>          Specify the diameter of the frame for PNG/PDF [default: 64]
   -c <file> --config=<file>        Override config file [default: iconframer.yaml]
   -h --help                        Show this screen.
   -v --version                     Show version.


Similar software
-----------------

* svglue
* pyconizr
