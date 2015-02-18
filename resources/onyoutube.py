import xbmc, xbmcgui, xbmcplugin
from resources.pytube import YouTube
from resources.rss import rss
from resources.xml_parser import xml_parser
import resources.config as config
import re

# list, show and play a subreddit
class onyoutube:
  def __init__(self, subreddit):
    self.subreddit = subreddit
  
  # get main listing
  def index(self):
    data = rss(self.subreddit).fetch()
    parser = xml_parser(data)
    for item in parser.xml_document().getElementsByTagName('item'):        
      title       = parser.element_text(item, 'title')
      thumbnail   = parser.attribute_value(item, 'media:thumbnail', 'url')
      description = parser.element_text(item, 'description')        
      match       = re.search('watch\?v=([a-zA-Z0-9_-]*)', description)
      if match:
        video_id  = match.group(1)
        self.add_dir(video_id, title, thumbnail)
      match       = re.search('\.be\/([a-zA-Z0-9_-]*)', description)
      if match:
        video_id  = match.group(1)
        self.add_dir(video_id, title, thumbnail)
    xbmcplugin.endOfDirectory(config.__id__)

  def add_dir(self, video_id, title, thumbnail):
    url       = "%s?subreddit=%s&video_id=%s" % (config.__plugin__, self.subreddit, video_id)
    listitem  = xbmcgui.ListItem(title, iconImage = "DefaultFolder.png", thumbnailImage = thumbnail)
    xbmcplugin.addDirectoryItem(handle = config.__id__, url = url, listitem = listitem,  isFolder = True)

  # show all streams for a video
  def show(self, video_id):    
    for index, video in self.videos(video_id):
      url         = "%s?subreddit=%s&video_id=%s&index=%s" % (config.__plugin__, self.subreddit, video_id, index)
      codec       = video.video_codec.encode('ASCII', 'ignore')
      resolution  = video.resolution.encode('ASCII', 'ignore')
      label       = "%s (%s)" % (resolution, codec)
      listitem    = xbmcgui.ListItem(label, iconImage = "DefaultFolder.png", thumbnailImage = "")
      xbmcplugin.addDirectoryItem(handle = config.__id__, url = url, listitem = listitem,  isFolder = True)
    xbmcplugin.endOfDirectory(config.__id__)

  # play the video stream
  def play(self, video_id, index):
    for index2, video in self.videos(video_id):
      if index == index2:
        url       = video.url
        listitem  = xbmcgui.ListItem(path = url)
        xbmc.Player().play(url, listitem, False, -1)

  # constuct full youtube url
  def full_url(self, video_id):
    full_url = "https://www.youtube.com/watch?v=%s" % video_id
    return full_url

  # get youtube streams
  def youtube(self, video_id):
    youtube     = YouTube()
    youtube.url = self.full_url(video_id)
    return youtube

  # create enumerable youtube videos
  def videos(self, video_id):
    return enumerate(self.youtube(video_id).videos)