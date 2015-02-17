import xbmcaddon, xbmcgui, xbmcplugin
import sys
import urllib2
import re
from xml.dom import minidom

__plugin__  = sys.argv[0]
__id__      = int(sys.argv[1])

# read RSS for subreddit
class rss:
  def __init__(self, subreddit):
    self.agent  = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16'
    self.url    = "%s/r/%s.rss" % ('http://www.reddit.com', subreddit)
    self.data   = ''

  def fetch(self):    
    opener = urllib2.build_opener()
    urllib2.install_opener(opener)
    request = urllib2.Request(self.url)
    request.add_header('User-agent', self.agent)
    try:
     response   = urllib2.urlopen(request, timeout = 20)
     self.data  = response.read()
     response.close()
    except urllib2.HTTPError, err:
      xbmc.log("urllib2.HTTPError requesting URL: %s" % (err.code))
    else:
      return self.data

# parse data into GUI folder
class parser:
  def __init__(self, data):
    self.data = data

  def to_gui(self, type = 'folder'):    
    if type == 'folder':      
      for item in self.xml_document().getElementsByTagName('item'):        
        title       = self.get_text(item.getElementsByTagName("title")[0].childNodes)
        thumbnail = ""
        try:
          thumbnail = item.getElementsByTagName('media:thumbnail')[0].attributes['url'].value
        except BaseException, err:
          xbmc.log("BaseException: %s" % err)
          thumbnail = ""
        description = self.get_text(item.getElementsByTagName("description")[0].childNodes)        
        match       = re.search('watch\?v=([a-zA-Z0-9]*)\"', description)
        if match:
          video_id  = match.group(1)
          url       = "%s?v=%s" % (__plugin__, video_id)
          listitem  = xbmcgui.ListItem(title, iconImage = "DefaultFolder.png", thumbnailImage = thumbnail)
          xbmcplugin.addDirectoryItem(handle = __id__, url = url, listitem = listitem,  isFolder = True)
      xbmcplugin.endOfDirectory(__id__)

  def xml_document(self):   
    return minidom.parseString(self.data).documentElement

  def get_text(self, nodelist):
    text = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            text.append(node.data)
    return ''.join(text).encode("ASCII", 'ignore')


# fullmoviesonyoutube subreddit
class fullmoviesonyoutube:
  def __init__(self):
    self.subreddit = 'fullmoviesonyoutube'
  
  def index(self):
    data = rss(self.subreddit).fetch()
    parser(data).to_gui('folder')

  def play(self, video_id):
    url = "https://www.youtube.com/watch%s" % video_id
    xbmc.log("-- url: %s" % url)
    listitem = xbmcgui.ListItem(path = url)
    xbmc.Player().play(url, listitem, False, -1)
    return(xbmcplugin.setResolvedUrl(handle = __id__, succeeded = True, listitem = listitem))

if sys.argv[2] == "":
  fullmoviesonyoutube().index()
else:
  fullmoviesonyoutube().play(sys.argv[2])