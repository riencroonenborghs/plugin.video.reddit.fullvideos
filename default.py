import xbmcaddon, xbmcgui, xbmcplugin
import sys, cgi
import urlparse
import resources.config as config
from resources.onyoutube import onyoutube
from resources.subreddits import subreddits

# MAIN
params = cgi.parse_qs(urlparse.urlparse(sys.argv[2])[4])

if params:
  subreddit_p = params.get('subreddit') != None
  video_id_p  = params.get('video_id') != None
  index_p     = params.get('index') != None
  
  if subreddit_p and not video_id_p and not index_p:
    subreddit = params['subreddit'][0]
    onyoutube(subreddit).index()
  if subreddit_p and video_id_p and not index_p:
    subreddit = params['subreddit'][0]
    video_id = params['video_id'][0]
    onyoutube(subreddit).show(video_id)
  if subreddit_p and video_id_p and index_p:
    subreddit = params['subreddit'][0]
    video_id = params['video_id'][0]
    index = params['index'][0]
    onyoutube(subreddit).play(video_id, int(index))
    
else:
  subreddits().index()