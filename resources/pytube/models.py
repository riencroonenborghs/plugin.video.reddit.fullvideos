# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from os.path import normpath, isfile
from os import remove
from time import clock
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
from .utils import sizeof
from os.path import isdir


class Video(object):
    """
    Class representation of a single instance of a YouTube video.

    """
    def __init__(self, url, filename, **attributes):
        """
        Define the variables required to declare a new video.

        Keyword arguments:
        extention -- The file extention the video should be saved as.
        resolution -- The broadcasting standard of the video.
        url -- The url of the video. (e.g.: youtube.com/watch?v=..)
        filename -- The filename (minus the extention) to save the video.
        """

        self.url = url
        self.filename = filename
        self.__dict__.update(**attributes)

    def download(self, path=None, chunk_size=8 * 1024,
                 on_progress=None, on_finish=None, force_overwrite=False):
        """
        Downloads the file of the URL defined within the class
        instance.

        Keyword arguments:
        path -- Destination directory
        chunk_size -- File size (in bytes) to write to buffer at a time
                      (default: 8 bytes).
        on_progress -- A function to be called every time the buffer was
                       written out. Arguments passed are the current and
                       the full size.
        on_finish -- To be called when the download is finished. The full
                     path to the file is passed as an argument.

        """

        if isdir(normpath(path)) :
            path = (normpath(path) + '/' if path else '')
            fullpath = '{0}{1}.{2}'.format(path, self.filename, self.extension)
        else:
            fullpath = normpath(path)

        # Check for conflicting filenames
        if isfile(fullpath) and not force_overwrite:
            raise BaseException("\n\nError: Conflicting filename:'{}'.\n\n".format(
                  self.filename))

        response = urlopen(self.url)
        meta_data = dict(response.info().items())
        file_size = int(meta_data.get("Content-Length") or
                        meta_data.get("content-length"))
        self._bytes_received = 0
        start = clock()
        try:
            with open(fullpath, 'wb') as dst_file:
                # Print downloading message
                print("\nDownloading: '{0}.{1}' (Bytes: {2}) \nto path: {3}\n\n".format(
                      self.filename, self.extension, sizeof(file_size), path))

                while True:
                    self._buffer = response.read(chunk_size)
                    if not self._buffer:
                        if on_finish:
                            on_finish(fullpath)
                        break

                    self._bytes_received += len(self._buffer)
                    dst_file.write(self._buffer)
                    if on_progress:
                        on_progress(self._bytes_received, file_size, start)

        # Catch possible exceptions occurring during download
        except IOError:
            raise IOError("\n\nError: Failed to open file.\n"
                  "Check that: ('{0}'), is a valid pathname.\n\n"
                  "Or that ('{1}.{2}') is a valid filename.\n\n".format(
                      path, self.filename, self.extension))

        except BufferError:
            raise BufferError("\n\nError: Failed on writing buffer.\n"
                  "Failed to write video to file.\n\n")

        except KeyboardInterrupt:
            remove(fullpath)
            raise KeyboardInterrupt("\n\nInterrupt signal given.\nDeleting incomplete video"
                  "('{0}.{1}').\n\n".format(self.filename, self.extension))

    def __repr__(self):
        """A cleaner representation of the class instance."""
        return "<Video: {0} (.{1}) - {2} - {3}>".format(
            self.video_codec,
            self.extension,
            self.resolution,
            self.profile)

    def __lt__(self, other):
        if type(other) == Video:
            v1 = "{0} {1}".format(self.extension, self.resolution)
            v2 = "{0} {1}".format(other.extension, other.resolution)
            return (v1 > v2) - (v1 < v2) < 0
