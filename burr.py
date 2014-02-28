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

def guess_type(filename):
  magic_guess = magic.from_file(filename)
  if magic_guess.startswith('gzip'):
    if filename.endswith('tgz') or filename.endswith('tar.gz'):
      return 'tar.gz'
    else:
      return 'gzip'
  elif magic_guess.startswith('bzip'):
    if filename.endswith('tbz2') or filename.endswith('tar.bz2'):
      return 'tar.bz2'
    else:
      return 'bzip'
  elif magic_guess.startswith('Zip'):
    return 'zip'

def list_contents(archive, arguments):
  a = archive[0]
  gt = guess_type(a)
  if gt in ['tar.gz', 'tar.bz2']:
    call(["tar", "-tf", a])
  elif gt == 'gzip':
    call(["gzip", "-l", a])
  elif gt == 'bzip':
    print("Error: bzip is not an archive format")
  elif gt == 'zip':
    call(["unzip", "-l", a])

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
