import os, gettext, sys
from xml.etree import ElementTree as etree
import polib
import yaml
import docopt

try:
   import cairo
   import rsvg
except:
   pass
   
template = "template.svg"
icondir = "icons"
outdir = "output"

NS = "http://www.w3.org/2000/svg"


def load_translations(pth, languages):
   installed = {}
   for l in languages:
      try:
         installed[l] = gettext.translation('iconframer', localedir=pth, languages=[l])
      except IOError:
         errpth = os.sep.join((pth, l, "LC_MESSAGES" + os.sep))
         err = "No 'iconframer.mo' file found at %s" % errpth
         sys.exit(err)
   return installed

   
def prepare_template(svgdata):
   "add elements to template"

   root = etree.fromstring(svgdata)
   w = float(root.attrib["width"])
   h = float(root.attrib["height"])

   lx = w/2
   ly = h-8
   fs = w/8

   labelnode = etree.Element(tag="{%s}text" % NS, id ="label", x=str(lx), y=str(ly), fill="white")
   labelnode.attrib["text-anchor"] = u"middle"
   labelnode.attrib["font-size"] = str(fs)
   labelnode.attrib["font-weight"] = "bold"
   labelnode.attrib["font-famiy"] = "Tahoma"
   
   root.append(labelnode)
   
   return root


def add_icon(template, icon, id):
    icon_elem = icon.find(".//g[@id='%s']" % id)   
    return icon_elem
    
   
def apply_data(template, label_id):
   labelnode = template.find(".//*[@id='label']")
   labelnode.text = label_id.upper()
   return template

def generate_png(svgstr, size, pngfilepath):
   ""
   img =  cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
   ctx = cairo.Context(img)
   handler= rsvg.Handle(None, svgstr)
   handler.render_cairo(ctx)
   ctx.scale(200.0/size, 200.0/size)
   img.write_to_png(pngfilepath)