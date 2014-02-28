#!/usr/bin/python

import sys, os, re
from optparse import OptionParser


opts = OptionParser(description="" +
    "This script is used to create a bookmarklet. It allows you to " +
    "write javascript bookmarklets with whitespace and comments " +
    "for readability and then run them through this script to strip " +
    "whitespace, escape characters, and remove comments. Then it " +
    "copies the prepared string of javascript to your clipboard so " +
    "you can paste it into a bookmark.")

opts.add_option('-f', '--filename', type='string', dest='filename', help="" +
    "This is the path to the javascript file that you want to create " +
    "the bookmarklet from. REQUIRED.")

(options, posArgs) = opts.parse_args()


if not options.filename:
    print "Error: A filename (-f argument) is required to run this script"
    exit()

if not os.path.exists(options.filename):
    print "Error: This file could not be found: %s" % options.filename
    exit()


def strip_comments_and_whitespace(str):
    array = []
    str = re.sub('/\*.*?\*/', '', str, 0, re.DOTALL);
    for i,it in enumerate(str.split('\n')):
        if it.find('//') > -1:
            it = it[:it.find('//')]
        array.append(''.join(it.split()))
    return ''.join(array)


def bookmarkify():
    f = options.filename
    f = open(f, 'r').read()
    f = strip_comments_and_whitespace(f)
    f = f.replace("\n", "").replace("\'", "\"").replace("\t", "").replace("var", "var ")
    f = "\'javascript:" + f + "\'"
    print f

    cmd = 'echo %s | tr -d "\n" | pbcopy' % f
    os.system(cmd)


bookmarkify()