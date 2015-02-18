import xbmc, xbmcgui, xbmcplugin
from resources.onyoutube import onyoutube
import resources.config as config
import json

# list and show available subreddits
class subreddits:
  def __init__(self):
    xbmc.log(config.__settings__.getSetting('subreddits'))
    if config.__settings__.getSetting('subreddits') == "":
      self.load_default_subreddits()
    else:
      self.load_subreddits_from_file(config.__settings__.getSetting('subreddits'))

  def load_default_subreddits(self):
    self.subreddits = dict()
    self.subreddits['Full Movies'] = 'fullmoviesonyoutube'
    self.subreddits['Full Foreign Movies'] = 'fullforeignmovies'
    self.subreddits['True Horror'] = 'truehorror'
    self.subreddits['Full SciFi Movies'] = 'fullscifimovies'
    self.subreddits['Audiobooks'] = 'AudiobooksonYouTube'
    self.subreddits['Full TVshows'] = 'FullTVshowsonYouTube'
    self.subreddits['Star Trek'] = 'StarTrekonYouTube'
    self.subreddits['Music Videos'] = 'MusicVideosonYouTube'
    self.subreddits['Full Concert'] = 'FullConcertonYouTube'
    self.subreddits['Full Albums'] = 'FullAlbumsonYouTube'
    self.subreddits['Soundtracks'] = 'SoundtracksonYouTube'
    self.subreddits['Bollywood'] = 'BollywoodonYouTube'
    self.subreddits['Kung Fu'] = 'KungFuonYouTube'
    self.subreddits['Full Cartoons'] = 'FullCartoonsonYouTube'
    self.subreddits['Full Anime'] = 'FullAnimeonYouTube'
    self.subreddits['Full Westerns'] = 'FullWesternsonYouTube'

  def load_subreddits_from_file(self, filename):
    json_data = open(filename)
    data = json.load(json_data)
    json_data.close()
    self.subreddits = data
  
  # get main listing
  def index(self):
    for title in self.subreddits:        
      subreddit = self.subreddits[title]
      url       = "%s?subreddit=%s" % (config.__plugin__, subreddit)
      listitem  = xbmcgui.ListItem(title, iconImage = "DefaultFolder.png", thumbnailImage = "")
      xbmcplugin.addDirectoryItem(handle = config.__id__, url = url, listitem = listitem,  isFolder = True)
    xbmcplugin.endOfDirectory(config.__id__)