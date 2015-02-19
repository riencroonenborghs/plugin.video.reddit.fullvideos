import xbmcaddon
import sys

__plugin__    = sys.argv[0]
__id__        = int(sys.argv[1])
__name__      = 'plugin.video.reddit.fullvideos'
__settings__  = xbmcaddon.Addon(id = __name__)

URL_LIST      = "%s?action=list&subreddit=%s"
URL_SHOW      = "%s?action=show&video_id=%s"
URL_PLAY      = "%s?action=play&video_id=%s&index=%s"
URL_DOWNLOAD  = "%s?action=download&video_id=%s&index=%s"
