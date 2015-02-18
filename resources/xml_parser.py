import xbmc
from xml.dom import minidom
import sys

# parse XML data and provide some helpers to make parsing it easier
# I'm sure there's better things out there
class xml_parser:
  def __init__(self, data):
    self.data = data

  def xml_document(self):   
    return minidom.parseString(self.data).documentElement

  def element_text(self, item, name):
    try:
      return self.text(item.getElementsByTagName(name)[0].childNodes)
    except BaseException, err:
      xbmc.log("BaseException: %s" % err)
      sys.stdout.write("BaseException: %s" % err)
    else:
      return ""

  def attribute_value(self, item, name, attribute):
    try:
      return item.getElementsByTagName(name)[0].attributes[attribute].value
    except BaseException, err:
      xbmc.log("BaseException: %s" % err)
      sys.stdout.write("BaseException: %s" % err)
    else:
      return ""

  def text(self, nodelist):
    text = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            text.append(node.data)
    return ''.join(text).encode("ASCII", 'ignore')