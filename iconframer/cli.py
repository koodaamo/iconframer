# -*- encoding:utf-8 -*-

"""
iconframer - a command-line tool to generate SVG icons from templates

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

"""

import codecs, os, gettext, sys, copy
from docopt import docopt
from xml.etree import ElementTree as etree
import lya
import polib

from iconframer import load_translations, prepare_template, add_label, add_icon, NS
from iconframer import convert_svg, process_path, find_colors, inverse_colors

def iconframer():

   args = docopt(__doc__, version='iconframer 1.0')
   conf = lya.AttrDict.from_yaml(args["--config"])

   # NEED CAIRO AND RSVG INSTALLED FOR PNG & PDF CONVERSION
   if args["png"] or args["pdf"]:
      try:
         import cairo
         import rsvg
      except ImportError:
         sys.exit("Need cairo and rsvg for PNG/PDF generation")

   # LANGUAGES & TRANSLATIONS
   languages = args["<language>"] or conf.get("languages")
   if not languages:
      sys.exit("need language to use")
   
   _i18npth = args.get("--translations") or conf.paths.get("translations")
   # custom default to i18n
   if not _i18npth:
      i18npth = process_path("i18n files", "i18n")
   else:
      i18npth = process_path("i18n files", _i18npth)

   translations = load_translations(i18npth, languages)
   
   # TEMPLATES
   tmpl_dir_pth = conf.paths.get("templates") + os.sep or ""

   _tmplp = conf.get("template")
   if _tmplp:
      _tmplp = _tmplp if _tmplp.endswith(".svg") else _tmplp + ".svg"
   tmpl_pth = process_path("svg template", tmpl_dir_pth + _tmplp)

   # IMAGES
   imgs_fn = conf.get("images") or ""
   if imgs_fn:
      if not imgs_fn.endswith(".svg"):
         imgs_fn = conf["images"] + ".svg"
   
   imgs_dir = conf.paths.get("images") + os.sep or ""
   imgs_pth = process_path("source images file", imgs_dir + imgs_fn)

   imgs_svg = etree.parse(imgs_pth)
   imgs = imgs_svg.find("./{%s}g[@id='Images']" % NS)

   # OUTPUT
   outdir = process_path("output dir", conf.paths.get("output"))

   # READ SVG
   with codecs.open(tmpl_pth, encoding="utf-8") as svgfile:
      svgdata = svgfile.read() 
   
   if translations:
      template = prepare_template(svgdata)

      pot = polib.pofile(i18npth + os.sep + "iconframer.pot", encoding="utf-8")
      icons = {}
      for entry in pot:
         icon = imgs.find("./*[@id='%s']" % entry.msgid)
         if icon is not None:
            icons[entry.msgid] = icon
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
            icon = icons[entry.msgid]

            # no label
            if not args["--nolabel"]:
               color = "black" if args["--inverse"] else "white"
               add_label(tmpl, _(entry.msgid), color)

            # inversion
            if args["--inverse"]:
               inverse_colors(icon, colors[0], colors[1])
            tmpl.append(icon)


            # write out files
            pthbase = outdir + os.sep + entry.msgid + "-" + lc + "."
            svgstr = etree.tostring(tmpl, encoding="UTF-8")

            if args["svg"]:
               with codecs.open(pthbase + "svg", "w") as out:
                  svgstr = etree.tostring(tmpl, encoding="UTF-8")
                  out.write(svgstr)
               
            if args["png"]:
               convert_svg(svgstr, int(args["--size"]), pthbase + "png", "PNG")
               
            if args["pdf"]:
               convert_svg(svgstr, int(args["--size"]), pthbase + "pdf", "PDF")
               
            print "Generated '%s'" % _(entry.msgid)
   

   
