# plugin.video.reddit.fullvideos

## What is it?

`plugin.video.reddit.fullvideos` is a video add-on for XBMC, or Kodi as it is called nowadays. Its aim is to let you watch [Youtube](http://www.youtube.com) videos, that have been posted on a number of subreddits on [Reddit](http://www.reddit.com).

## Installation

1. `git clone` this repository
2. `zip` the repository and put it somewhere where your XBMC/Kodi can find it. I highly recommend adding the version to your zip file name to avoid clashes when you update.
3. Install the zip through `Settings > Add-ons > Install from zip file`
4. Go to `Videos > Add-ons > Reddit's /r/_X_onyoutube` and start browsing

## Configuration

### Topics

By default `plugin.video.reddit.fullvideos` lists all posts by `Hot` topic. This can be changed. Available topics are `Hot`, `New`, `Rising` and `Top`. 

You can find the configuration at `Settings > Add-ons > Enable Add-ons > Video Add-ons > Reddit's /r/_X_onyoutube > Configure > Topic`

### Default subreddits

`plugin.video.reddit.fullvideos` comes with these subreddits out of the box:
- [/r/fullmoviesonyoutube](http://www.reddit.com/r/fullmoviesonyoutube)
- [/r/fullforeignmovies](http://www.reddit.com/r/fullforeignmovies)
- [/r/truehorror](http://www.reddit.com/r/truehorror)
- [/r/fullscifimovies](http://www.reddit.com/r/fullscifimovies)
- [/r/AudiobooksonYouTube](http://www.reddit.com/r/AudiobooksonYouTube)
- [/r/FullTVshowsonYouTube](http://www.reddit.com/r/FullTVshowsonYouTube)
- [/r/StarTrekonYouTube](http://www.reddit.com/r/StarTrekonYouTube)
- [/r/MusicVideosonYouTube](http://www.reddit.com/r/MusicVideosonYouTube)
- [/r/FullConcertonYouTube](http://www.reddit.com/r/FullConcertonYouTube)
- [/r/FullAlbumsonYouTube](http://www.reddit.com/r/FullAlbumsonYouTube)
- [/r/SoundtracksonYouTube](http://www.reddit.com/r/SoundtracksonYouTube)
- [/r/BollywoodonYouTube](http://www.reddit.com/r/BollywoodonYouTube)
- [/r/KungFuonYouTube](http://www.reddit.com/r/KungFuonYouTube)
- [/r/FullCartoonsonYouTube](http://www.reddit.com/r/FullCartoonsonYouTube)
- [/r/FullAnimeonYouTube](http://www.reddit.com/r/FullAnimeonYouTube)
- [/r/FullWesternsonYouTube](http://www.reddit.com/r/FullWesternsonYouTube)

### Custom subreddits

You can set your custom list of subreddits. This can be done by configuring the add-on in `Settings > Add-ons > Enable Add-ons > Video Add-ons > Reddit's /r/_X_onyoutube > Configure > Subreddits file`. A JSON file can be selected containing a list of your custom subreddits.

The format of the JSON file should be: `{"Name of subreddit 1":"subreddit_1","Name of subreddit 2":"subreddit_2",...}`
Note that the `subreddit` part is without `/r/`! 

Example JSON file: `{"Full Movies":"fullmoviesonyoutube","Full Foreign Movies":"fullforeignmovies"}`

### Downloads

You can set a directory where your files will be downloaded to, if you choose to do so.

Not that I'm endorsing this.

At all.

## Internals

A quick note on the internals of the add-on. When checking the posts, it will look for the `description` in the subreddit's RSS and parse any [Youtube](http://www.youtube.com)-looking URLs.

## Credits

Many thanks to [pytube](https://github.com/nficano/pytube) to alleviate most of the hard work :)