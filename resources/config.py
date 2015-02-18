import xbmcaddon
import sys

__plugin__    = sys.argv[0]
__id__        = int(sys.argv[1])
__name__      = 'plugin.video.reddit.fullvideos'
__settings__  = xbmcaddon.Addon(id = __name__)
