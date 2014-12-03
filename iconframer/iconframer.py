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
   
NS = "http://www.w3.org/2000/svg"

INVERSABLES = ("path", "rect", "text", "tspan")


def stripns(nstag):
   ""
   return nstag[nstag.index("}")+1:]


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
   "load SVG"
   root = etree.fromstring(svgdata)
   return root

def add_icon(template, icon, id):
    icon_elem = icon.find(".//g[@id='%s']" % id)   
    return icon_elem
    
   
def add_label(template, label_id, color):

   w = float(template.attrib["width"])
   h = float(template.attrib["height"])

   fs = w/8
   lx = w/2
   ly = h-(fs/2.0)+fs/5.0

   
   labelnode = etree.Element(tag="{%s}text" % NS, id ="label", x=str(lx), y=str(ly), fill=color)
   labelnode.attrib["text-anchor"] = u"middle"
   labelnode.attrib["font-size"] = str(fs)
   labelnode.attrib["font-weight"] = "bold"
   labelnode.attrib["font-family"] = "sans-serif"
   labelnode.text = label_id.upper()
   template.append(labelnode)
   return template


def find_colors(images):
   ""
   elms = []
   colors = []
   for image in images:
      for tag in INVERSABLES:
         elms.extend(image.findall(".//{%s}%s" % (NS, tag)))

   fills = [elm.attrib["fill"].strip().upper() for elm in elms if elm.attrib.get("fill")]
   strokes = [elm.attrib["stroke"].strip().upper() for elm in elms if elm.attrib.get("stroke")]
   colors = set(fills).union(strokes)
   return list(colors)


def inverse_element(elm, col1, col2):

   tag = elm.tag[elm.tag.index("}")+1:]

   fill = elm.attrib.get("fill")
   stroke = elm.attrib.get("stroke")

   if fill == col1:
      elm.attrib["fill"] = col2
      print " inverted %s fill from %s to %s" % (tag, fill, col2)
   elif fill == col2:
      elm.attrib["fill"] = col1
      print " inverted %s fill from %s to %s" % (tag, fill, col1)
   else:
      if fill:
         sys.exit("fill %s of %s not either %s or %s" % (fill, tag, col1, col2))

   if stroke == col1:
      elm.attrib["stroke"] = col2
      print " inverted %s stroke from %s to %s" % (tag, stroke, col2)
   elif stroke == col2:
      elm.attrib["stroke"] = col1
      print " inverted %s stroke from %s to %s" % (tag, stroke, col1)
   else:
      if stroke:
         sys.exit("stroke %s of %s not either %s or %s" % (stroke, tag, col1, col2))

      
def inverse_colors(image, col1, col2):
   print "Inverting %s:" % image.attrib.get("id")

   if stripns(image.tag) != "g":
      inverse_element(image, col1, col2)

   for tag in INVERSABLES:
      elms = image.findall(".//{%s}%s" % (NS, tag))
      for elm in elms:
         inverse_element(elm, col1, col2)


def generate_png(svgstr, size, pngfilepath):
   ""
   img =  cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
   ctx = cairo.Context(img)
   handler= rsvg.Handle(None, svgstr)
   iw,ih, fw,fh =  handler.get_dimension_data()
   ctx.translate(0,0)
   ctx.scale(size/fw, size/fh) # assumes bigger source SVG template
   handler.render_cairo(ctx)
   img.write_to_png(pngfilepath)
