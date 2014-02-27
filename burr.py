#!/usr/bin/env python

"""burr

Usage:
  burr pack <destination> <file> ...
  burr unpack <archive> ...
  burr list <archive>
  burr [+tar|+bz2|+gz|+lz|+lzma|+zip|+7z|+tgz|+tar.gz] <file>
  burr (-h | --help | --version)

Commands:
  pack          Create a new <destination> archive and add <file>s to it
  unpack        Unpack all files in <archive> to current folder
  list          List contents of <archive>

  A +<format> command compresses <file>.
  If no commands are matched, burr unpacks the given file

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from subprocess import call
from docopt import docopt
import magic

def list_contents(archive, arguments):
  a = archive[0]
  filetype = magic.from_file(a)
  if filetype.startswith('gzip'):
    call(["tar", "-tf", archive[0]])

if __name__ == '__main__':
    arguments = docopt(__doc__, version='burr 0.1')
    print arguments
    if arguments['pack']:
      print("create destination file %s" % arguments['<destination>'])
      print("adding files %s" % arguments['<file>'])
    if arguments['unpack']:
      print("unpacking %s" % arguments['<archive>'])
    if arguments['list']:
      list_contents(arguments['<archive>'], arguments)
