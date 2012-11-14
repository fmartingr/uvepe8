#!/usr/bin/env python
# -*- coding: utf-8 -*-

###
# UVEPE8
# Author:       Felipe "Pyron" Martín (@fmartingr)
# Usage:		uvepe8.py -h
# Notes:		See README
###

import argparse
from controller import FrameController, DiffController
import glob
from sys import stdout

def echo(string, cr=True, newline=True):
    """
    Custom print function
    cr = prints carriage return (before string!)
    newline = prints newline
    """
    if cr: stdout.write("\r")
    stdout.write(string)
    if newline: stdout.write("\n")

parser = argparse.ArgumentParser(description="Your videos, now in <canvas>", )

# Required arguments
parser.add_argument('folder', help="Folder with the PNG frames", )
parser.add_argument('name', help="Animation name", )

# Optional arguments
#parser.add_argument('-m', '--diff-method', default="Simple",
#    help="Diff method (default: Simple)",
#    choices=['Simple'])
parser.add_argument('-fps', default=30, help="FPS (default: 30)", )
parser.add_argument('-t', '--filetype', default="png", help="Frame filetype (default png)")
parser.add_argument('-c', '--compress', help="Compress PNG with pngcrush", action="store_true", )

# Parsing
argument = parser.parse_args()

# Trailing slash fix
if argument.folder[-1] is "/":
    argument.folder = argument.folder[:-1]

# Getting files info
PATH = "%s/*.%s" % (argument.folder, argument.filetype)
FILES = glob.glob(PATH)
TOTAL_FILES = len(FILES)

if TOTAL_FILES is 0:
    print "Cannot find frames on that folder: %s" % PATH
    quit(1)

# Staring the controllers
FRAMES = FrameController()
DIFFS = DiffController()

# Starting the loop
CURRENT_FILE = 1
echo("%10s %8s " % ("FRAMES", "DIFFS"))
for file in FILES:
    if FRAMES.current is -1:
        # First frame, just append it.
        FRAMES.append(file)
    else:
        # Checking for diffs. Bitches LOVE diffs.
        FRAMES.append(file)
        diffs = FRAMES.get_current().get_difference()
        if not diffs:
            # If frame dont have any difference with the previous one
            # just add a frame jump in the previous frame.
            # The player will handle the rest.
            FRAMES.get_previous().jump += 1
            FRAMES.remove(FRAMES.get_current())
        else:
            # Ooops. We found some diffs.
            for diff in diffs:
                # Checking if we have something similar in our diff list.
                diff_number = DIFFS.find_hash(diff['hash'])
                if diff_number is None:
                    # If not... just append it.
                    DIFFS.append(diff)
                    diff_number = DIFFS.current
                # Assign the diff list key to the current frame
                FRAMES.get_current().diff.append(diff_number)
    # Pretty logging is pretty. <3
    echo("%10s %8s Processing..." % ("%d/%d" % (CURRENT_FILE, TOTAL_FILES), len(DIFFS.items)), True, False)
    CURRENT_FILE += 1

# Summary
print ""
print "-- Summary --"
print "Total frames: %d" % TOTAL_FILES
print "Total frames saved: %d" % len(FRAMES.items)
print "Total diffs saved: %d" % len(DIFFS.items)
print ""

class DiffMatrix(object):
    # http://codeincomplete.com/posts/2011/5/7/bin_packing/
    min_x = 0
    min_y = 0

    max_x = 0
    max_y = 0

    nodes = [] # (diff key, x, y, size x, size y)

    def __init__(self, width=0, height=0):
        self.max_x = width
        self.max_y = height

    def add_node(self, node):
        # node: (diff key, x, y, size x, size y)
        self.nodes.append(node)

    def find_position(self, size_x, size_y):

        pass

    def is_occupied(self, x, y):
        for node in self.nodes:
            # Check if pixel is inside this node's square
            if node[1] <= x <= node[1] + node[3]:
                if node[2] <= y <= node[2] + node[4]:
                    return True
        return False


# Sort DIFFs by size
DIFFS.sort_by_size()

for diff in DIFFS.items:
    pass
    #print diff.hash
    #diff.image.save("../diff/" + diff.hash + '.png')

if DIFFS.total['width'] >= DIFFS.total['height']:
    MATRIX = DiffMatrix(width=DIFFS.total['width'])
else:
    MATRIX = DiffMatrix(height=DIFFS.total['height'])



