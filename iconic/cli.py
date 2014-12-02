# -*- encoding:utf-8 -*-

"""
iconic - a command-line tool to generate SVG icons from templates

Usage:
  iconic [--config=<file>]
  iconic -h | --help
  iconic --version


Options:
  --config=<file>     Override config file [default: iconic.yaml]
  -h --help           Show this screen.
  -v --version        Show version.

"""

import codecs, os, gettext, sys, copy
from docopt import docopt
from xml.etree import ElementTree as etree
import lya
import polib

from iconic import load_translations, prepare_template, apply_data, add_icon, NS


def iconic():

   args = docopt(__doc__, version='iconic 1.0')
   conf = lya.AttrDict.from_yaml(args["--config"])
   
   if conf.paths.get("translations") and conf.get("languages"):
      i18npth = os.getcwd() + os.sep + conf.paths.translations
      translations = load_translations(i18npth, conf.languages)
   else:
      translations = None

   tmpldir = conf.paths.get("templates")
   tmpl = conf.get("template")
   if not (tmpldir and tmpl):
      sys.exit("need template path and name")
   
   imgs_fn = conf.get("images")
   if not os.path.exists(imgs_fn + ".svg"):
      sys.exit("no source images file found")
   imgs_svg = etree.parse(os.getcwd() + os.sep + imgs_fn + ".svg")
   imgs = imgs_svg.find("./{%s}g[@id='Images']" % NS)

   outdir = os.getcwd() + os.sep + conf.paths.get("output")
   if not conf.paths.get("output") or not os.path.isdir(outdir):
      sys.exit("invalid output dir given")

   tmpl = tmpl if tmpl.endswith(".svg") else tmpl + ".svg"
   with codecs.open(tmpldir + os.sep + tmpl, encoding="utf-8") as svgfile:
      svgdata = svgfile.read() 

   if translations:
      template = prepare_template(svgdata)

      pot = polib.pofile(i18npth + os.sep + "iconic.pot", encoding="utf-8")
      icons = {}
      for entry in pot:
         img = imgs.find("./*[@id='%s']" % entry.msgid)
         if img is not None:
            icons[entry.msgid] = img
         else:
            print "No image found for %s" % entry.msgid

      for lc in translations:
         gettext.install("iconic", i18npth, unicode=True)
         for entry in [e for e in pot if e.msgid in icons]:
            tmpl = copy.deepcopy(template)
            apply_data(tmpl, _(entry.msgid))
            tmpl.append(icons[entry.msgid])
            with codecs.open(outdir + os.sep + entry.msgid + "-fi.svg", "w") as out:
               out.write(etree.tostring(tmpl, encoding="UTF-8"))
               print "Generated '%s'" % _(entry.msgid)
   

   