# -*- encoding:utf-8 -*-

"""
iconframer - a command-line tool to generate SVG icons from templates

Usage:
  iconframer [--config=<file>] [(--png --size=<size>)] [-n --nolabel] [-i --inverse]
  iconframer -h | --help
  iconframer --version


Options:
  -p --png            Generate PNG bitmaps
  -i --inverse        Inverse the icon colors
  --size=<size>       Specify the diameter of the frame for PNG [default: 24]
  --config=<file>     Override config file [default: iconframer.yaml]
  -h --help           Show this screen.
  -v --version        Show version.

"""

import codecs, os, gettext, sys, copy
from docopt import docopt
from xml.etree import ElementTree as etree
import lya
import polib

from iconframer import load_translations, prepare_template, add_label, add_icon, NS
from iconframer import generate_png, find_colors, inverse_colors

def iconframer():

   args = docopt(__doc__, version='iconframer 1.0')
   conf = lya.AttrDict.from_yaml(args["--config"])

   if args["--png"]:
      try:
         import cairo
         import rsvg
      except ImportError:
         sys.exit("Need cairo and rsvg for PNG generation")

   if conf.paths.get("translations") and conf.get("languages"):
      i18npth = conf.paths.translations
      if i18npth[0] not in ('.','/'):
         i18npth = os.getcwd() + os.sep + i18npth
      translations = load_translations(i18npth, conf.languages)
   else:
      translations = {}

   tmpldir = conf.paths.get("templates")
   tmpl = conf.get("template")
   if not (tmpldir and tmpl):
      sys.exit("Need template path and name")
   
   imgs_fn = conf.get("images")
   imgs_dir = conf.paths.get("images")
   if not (imgs_fn and imgs_dir):
      sys.exit("Need source images path and name")

   imgs_pth = os.sep.join((os.getcwd(), imgs_dir, imgs_fn + ".svg"))
 
   if not os.path.exists(imgs_pth):
      sys.exit("No source images file found")
   imgs_svg = etree.parse(imgs_pth)
   imgs = imgs_svg.find("./{%s}g[@id='Images']" % NS)

   outdir = os.getcwd() + os.sep + conf.paths.get("output")
   if not conf.paths.get("output") or not os.path.isdir(outdir):
      sys.exit("Invalid output dir given")

   tmpl = tmpl if tmpl.endswith(".svg") else tmpl + ".svg"
   with codecs.open(tmpldir + os.sep + tmpl, encoding="utf-8") as svgfile:
      svgdata = svgfile.read() 

   if translations:
      template = prepare_template(svgdata)

      pot = polib.pofile(i18npth + os.sep + "iconframer.pot", encoding="utf-8")
      icons = {}
      for entry in pot:
         img = imgs.find("./*[@id='%s']" % entry.msgid)
         if img is not None:
            icons[entry.msgid] = img
         else:
            print "No image found for %s" % entry.msgid

      colors = find_colors(icons.values())
      if len(colors) > 2:
         sys.exit("more than 2 colors found in images!")
      print "Colors found: %s\n" % colors

      for lc in translations:
         _ = translations[lc].ugettext
         for entry in [e for e in pot if e.msgid in icons]:
            tmpl = copy.deepcopy(template)
            if not args["--nolabel"]:
               color = "black" if args["--inverse"] else "white"
               add_label(tmpl, _(entry.msgid), color)
            tmpl.append(icons[entry.msgid])
            if args["--inverse"]:
               inverse_colors(icons[entry.msgid], colors[0], colors[1])
            with codecs.open(outdir + os.sep + entry.msgid + "-fi.svg", "w") as out:
               svgstr = etree.tostring(tmpl, encoding="UTF-8")
               out.write(svgstr)
               if args["--png"]:
                  pngfilepath = outdir + os.sep + entry.msgid + "-fi.png"
                  generate_png(svgstr, int(args["--size"]), pngfilepath)
               print "Generated '%s'" % _(entry.msgid)
   

   
