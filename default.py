import xbmcaddon, xbmcgui, xbmcplugin, xbmc
import sys, cgi
import urlparse
import resources.config as config
from resources.onyoutube import onyoutube
from resources.subreddits import subreddits

# MAIN
params = cgi.parse_qs(urlparse.urlparse(sys.argv[2])[4])

if params:
  if params['action'][0] == 'list':
    subreddit = params['subreddit'][0]
    onyoutube().index(subreddit)
  elif params['action'][0] == 'show':
    video_id = params['video_id'][0]
    onyoutube().show(video_id)
  elif params['action'][0] == 'play':
    video_id  = params['video_id'][0]
    index     = int(params['index'][0])
    onyoutube().play(video_id, index)
  elif params['action'][0] == 'download':
    video_id  = params['video_id'][0]
    index     = int(params['index'][0])
    onyoutube().download(video_id, index)
else:
  subreddits().index()  