#!/usr/bin/python

from optparse import OptionParser
import sys

parser = OptionParser()
parser.add_option("-c","--char",
                  dest="chars",
                  action="store_true",
                  default=False,
                  help="only count chars"
                )
parser.add_option("-l","--line",
                  dest="lines",
                  action="store_true",
                  default=False,
                  help="only count lines"
                )
parser.add_option("-w","--word",
                  dest="words",
                  action="store_true",
                  default=False,
                  help="only count words"
                )
                
options, args = parser.parse_args()
if not (options.lines or options.words or options.chars):
    options.lines, options.words, options.chars = True, True, True
if args:
    fn = args[0]
    with open(fn) as fd:
        data = fd.read()
else:
    fn = ''
    data = sys.stdin.read()
chars = len(data)
lines = data.count('\n')
words = len(data.split())

if options.lines:
    print lines,
if options.words:
    print words,
if options.chars:
    print chars,   
