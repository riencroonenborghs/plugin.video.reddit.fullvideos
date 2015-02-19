import xbmc, xbmcgui, xbmcplugin
from resources.pytube import YouTube
from resources.rss import rss
from resources.xml_parser import xml_parser
import resources.config as config
import re, gc

# list, show and play a subreddit
class onyoutube:
  def __init__(self):
    self.cached_youtube_object  = None
    self.cached_videos          = None

  # get main listing
  def index(self, subreddit):
    data    = rss(subreddit).fetch()
    parser  = xml_parser(data)
    for item in parser.xml_document().getElementsByTagName('item'):        
      title       = parser.element_text(item, 'title')
      thumbnail   = parser.attribute_value(item, 'media:thumbnail', 'url')
      description = parser.element_text(item, 'description')        
      match       = re.search('watch\?v=([a-zA-Z0-9_-]*)', description)
      if match:
        video_id  = match.group(1)
        url       = config.URL_SHOW % (config.__plugin__, video_id)
        self.add_folder(url, title, thumbnail)
      match       = re.search('\.be\/([a-zA-Z0-9_-]*)', description)
      if match:
        video_id  = match.group(1)
        url       = config.URL_SHOW % (config.__plugin__, video_id)
        self.add_folder(url, title, thumbnail)
    xbmcplugin.endOfDirectory(config.__id__)

  # show all streams for a video
  def show(self, video_id):   
    for index, video in self.videos(video_id):
      codec           = video.video_codec.encode('ASCII', 'ignore')
      resolution      = video.resolution.encode('ASCII', 'ignore')
      play_url        = config.URL_PLAY % (config.__plugin__, video_id, index)
      play_label      = "Play video in %s (%s)" % (resolution, codec)
      download_url    = config.URL_DOWNLOAD % (config.__plugin__, video_id, index)
      download_label  = "Download video in %s (%s)" % (resolution, codec)
      self.add_play_video(play_url, play_label)
      self.add_download_video(download_url, download_label)
    xbmcplugin.endOfDirectory(config.__id__)

  # play the video stream
  def play(self, video_id, index):    
    for index2, video in self.videos(video_id):      
      if index == index2:        
        url       = video.url        
        listitem  = xbmcgui.ListItem(path = url)
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Preparing Your Video,3000)")
        xbmc.sleep(1000)
        xbmc.Player().play(url, listitem, False, -1)

  # download the video stream
  def download(self, video_id, index):
    download_path = config.__settings__.getSetting('downloads')
    for index2, video in self.videos(video_id):
      if index == index2:
        try:
          dialog  = xbmcgui.DialogProgressBG()
          dialog.create('Downloading %s' % video.filename)
          dialog.update(1)
          on_progress = lambda current_size, full_size, start: dialog.update(percent = int((current_size / float(full_size)) * 100))
          video.download(download_path, on_progress = on_progress)
          dialog.update(100, heading = 'Downloaded!')
          xmbc.sleep(1000)
          dialog.close()
        except BaseException, err:
          xbmc.log("ERROR: %s" % err)
          xbmc.executebuiltin("XBMC.Notification(Error!,%s,3000)" % err)

  def progress_update(self, current_size, full_size):
    return full_size / current_size
        

  # GUI related
  def add_list_item(self, url, title, thumbnail, icon, folder):
    listitem  = xbmcgui.ListItem(title, iconImage = icon, thumbnailImage = thumbnail)
    xbmcplugin.addDirectoryItem(handle = config.__id__, url = url, listitem = listitem,  isFolder = folder)       
  def add_folder(self, url, title, thumbnail):
    self.add_list_item(url, title, thumbnail, "DefaultFolder.png", True)
  def add_play_video(self, url, title):
    self.add_list_item(url, title, '', "DefaultVideo.png", False)  
  def add_download_video(self, url, title):
    self.add_list_item(url, title, '', "DefaultHardDisk.png", False)

    
  # constuct full youtube url
  def full_url(self, video_id):
    full_url = "https://www.youtube.com/watch?v=%s" % video_id
    return full_url

  # get youtube streams
  def youtube(self, video_id):
    if self.cached_youtube_object == None:
      youtube_object     = YouTube()
      youtube_object.url = self.full_url(video_id)
      self.cached_youtube_object = youtube_object
    return self.cached_youtube_object

  # create enumerable youtube videos
  def videos(self, video_id):
    if self.cached_videos == None:
      self.cached_videos = self.youtube(video_id).videos
    return enumerate(self.cached_videos)