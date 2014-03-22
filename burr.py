#!/usr/bin/env python

"""burr

Usage:
  burr pack <destination> <files> ...
  burr unpack <archive> ...
  burr list <archive>
  burr [+tar|+bz2|+gz|+lz|+lzma|+zip|+7z|+tgz|+tar.gz] <file>
  burr (-h | --help | --version)

Commands:
  pack          Create a new <destination> archive and add <file>s to it.
  unpack        Unpack all files in <archive> to current folder
  list          List contents of <archive>

  A +<format> command compresses <file>.
  If no commands are matched, burr unpacks the given file

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

#unpack-here
#unpack-all

from subprocess import call as old_call
from docopt import docopt
import magic

def call(*args):
  old_call(args)

def guess_type(filename):
  magic_guess = magic.from_file(filename)

  if magic_guess.startswith('gzip'):
    if filename.endswith('tgz') or filename.endswith('tar.gz'):
      return 'tar.gz'
    else:
      return 'gzip'
  if magic_guess.startswith('bzip'):
    if filename.endswith('tbz2') or filename.endswith('tar.bz2'):
      return 'tar.bz2'
    else:
      return 'bzip'
  if magic_guess.startswith('Zip'):
    return 'zip'
  if magic_guess.startswith('POSIX tar'):
    return 'tar'

  return "error: cannot guess file type"

def list_contents(arguments):
  a = arguments['<archive>'][0]
  gt = guess_type(a)
  if gt in ['tar.gz', 'tar.bz2', 'tar']:
    call("tar", "-tf", a)
  elif gt == 'gzip':
    call("gzip", "-l", a)
  elif gt == 'bzip':
    print("Warning: bzip is not an archive format")
  elif gt == 'zip':
    call("unzip", "-l", a)
  else:
    print "error: return value of guess_type not recognized: %s" % gt

def unpack(arguments):
  archives = arguments['<archive>']
  for archive in archives:
    gt = guess_type(archive)
    if gt == 'tar.gz':
      call("tar", "-xzf", archive)
    elif gt == 'tar':
      call("tar", "-xf", archive)
    elif gt == 'gzip':
      call("gzip", "-d", archive)

def pack(arguments):
  dest = arguments['<destination>']
  splitted = dest.split('.')
  if splitted[-2] == 'tar':
    end = "tar.%s" % splitted[-1]
  else:
    end = splitted[-1]

  files = arguments['<files>']
  if end == 'tar':
    old_call(["tar", "-cf", dest] + files)
  if end in ['tar.gzip', 'tar.gz', 'tgz']:
    old_call(["tar", "-czf", dest] + files)
  if end == 'gz':
    if len(files) > 1:
      print "error: gzip is not a container format"
    else:
      call("gzip", '-k', files[0])
      call("mv", "%s.gz" % files[0], dest)

arguments = docopt(__doc__, version='burr 0.1')

if arguments['pack']:
  pack(arguments)
elif arguments['unpack']:
  unpack(arguments)
elif arguments['list']:
  list_contents(arguments)
elif arguments['<file>']:
  print "switching to short mode..."
else:
  print "no command specified"