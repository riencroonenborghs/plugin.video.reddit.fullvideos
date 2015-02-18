import xbmc
import urllib2, sys
import resources.config as config

# read RSS feed for subreddit
class rss:
  def __init__(self, subreddit):
    self.agent  = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16'
    if config.__settings__.getSetting('topic') == 'Hot':
      self.url    = "%s/r/%s.rss" % ('http://www.reddit.com', subreddit)
    elif config.__settings__.getSetting('topic') == 'New':
      self.url    = "%s/r/%s/new/.rss" % ('http://www.reddit.com', subreddit)
    elif config.__settings__.getSetting('topic') == 'Rising':
      self.url    = "%s/r/%s/rising/.rss" % ('http://www.reddit.com', subreddit)
    elif config.__settings__.getSetting('topic') == 'Top':
      self.url    = "%s/r/%s/top/.rss" % ('http://www.reddit.com', subreddit)
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
      sys.stdout.write("urllib2.HTTPError requesting URL: %s" % (err.code))
    else:
      return self.data