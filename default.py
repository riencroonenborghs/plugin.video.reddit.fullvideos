import xbmcaddon, xbmcgui, xbmcplugin
import sys, cgi, re
import urllib2, urlparse
from xml.dom import minidom
from resources.pytube import YouTube

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
          url       = "%s?video_id=%s" % (__plugin__, video_id)
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
  
  # get main listing
  def index(self):
    data = rss(self.subreddit).fetch()
    parser(data).to_gui('folder')

  # list all streams for a video
  def list(self, video_id):    
    for index, video in self.videos(video_id):
      url       = "%s?video_id=%s&index=%s" % (__plugin__, video_id, index)
      listitem  = xbmcgui.ListItem(video.video_codec, iconImage = "DefaultFolder.png", thumbnailImage = "")
      xbmcplugin.addDirectoryItem(handle = __id__, url = url, listitem = listitem,  isFolder = True)
    xbmcplugin.endOfDirectory(__id__)

  # play the video stream
  def play(self, video_id, index):
    for index2, video in self.videos(video_id):
      if index == index2:
        # video     = self.videos(video_id)[index]
        url       = video.url
        listitem  = xbmcgui.ListItem(path = url)
        xbmc.Player().play(url, listitem, False, -1)
        return(xbmcplugin.setResolvedUrl(handle = __id__, succeeded = True, listitem = listitem))

  def full_url(self, video_id):
    full_url = "https://www.youtube.com/watch?v=%s" % video_id
    return full_url

  def youtube(self, video_id):
    youtube     = YouTube()
    youtube.url = self.full_url(video_id)
    return youtube

  def videos(self, video_id):
    return enumerate(self.youtube(video_id).videos)


# MAIN
params = cgi.parse_qs(urlparse.urlparse(sys.argv[2])[4])
if params:
  if params.get('video_id') != None:
    if params.get('index') == None:
      fullmoviesonyoutube().list(params['video_id'][0])
    else:
      fullmoviesonyoutube().play(params['video_id'][0], int(params['index'][0]))
else:
  fullmoviesonyoutube().index()