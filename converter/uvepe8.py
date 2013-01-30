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
import Image
#from random import randint
import json


def echo(string, cr=True, newline=True):
    """
    Custom print function
    cr = prints carriage return (before string!)
    newline = prints newline
    """
    if cr:
        stdout.write("\r")
    stdout.write(string)
    if newline:
        stdout.write("\n")
    stdout.flush()

parser = argparse.ArgumentParser(description="Your videos, now in <canvas>", )

# Required arguments
parser.add_argument('folder', help="Folder with the PNG frames", )
parser.add_argument('name', help="Animation name", )

# Optional arguments
parser.add_argument('-m', '--diff-method', default="Simple",
    help="Diff method (default: Simple)",
    choices=['Simple', 'Grid'])
parser.add_argument('-fps', default=30, help="FPS (default: 30)", )
parser.add_argument('-t', '--filetype', default="png", help="Frame filetype (default png)")
parser.add_argument('-c', '--compress', help="Compress PNG with pngcrush", action="store_true", )

# Optional arguments for Grid method
#parser.add_argument('--squaresize', default="2,2", help="GridMethod: Square size for portions")

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
FRAMES = FrameController(argument.diff_method)
DIFFS = DiffController()

# Starting the loop
CURRENT_FILE = 1
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
                # Assign the diff hash to the current frame
                FRAMES.get_current().add_diff((diff['hash'],
                                              diff['position'][0],
                                              diff['position'][1],
                                              diff['size'][0],
                                              diff['size'][1]))
    # Pretty logging is pretty. <3
    echo("Processing frame (%s)" % ("%d/%d" % (CURRENT_FILE, TOTAL_FILES)), True, False)
    CURRENT_FILE += 1

# Summary
print ""
print "-- Summary --"
print "Total frames: %d" % TOTAL_FILES
print "Total frames saved: %d" % len(FRAMES.items)
print "Total diffs saved: %d" % len(DIFFS.items)
print "-------------"
print ""


class DiffMatrix(object):
    min_x = 0
    min_y = 0

    max_x = 0
    max_y = 0

    squares = []  # (diff key, x, y, size x, size y)

    algorithm = None
    controller = None

    def __init__(self, width=0, height=0, algorithm='BinaryTree', controller=None):
        # Load algorithm
        module = __import__("algorithm")
        try:
            algorithm = getattr(module, "%sAlgorithm" % algorithm)
        except Exception:
            print "Cant load %s algorithm, using BinaryTree..." % algorithm
            algorithm = getattr(module, "BinaryTreeAlgorithm")
        self.max_x = width
        self.max_y = height
        self.algorithm = algorithm(self.max_x, self.max_y)
        if controller is not None:
            self.controller = controller

    def add(self, diff):
        """
        Uses the selected algorithm to add a diff image to the group
        diff = tuple(diff key, width, height)
        """
        self.squares.append(self.algorithm.append(diff))

    def create_image(self):
        final_image = Image.new('RGBA', self.algorithm.get_total_size())
        for square in self.squares:
            if square[0] == "first_frame":
                box = (0, 0)
                image = FRAMES.items[0].image
            else:
                diff = self.controller.items[self.controller.find_hash(square[0])]
                diff.set_position(square[1], square[2])
                box = (square[1], square[2], square[1] + diff.size[0], square[2] + diff.size[1])
                image = diff.image
                #final_image.paste((randint(0, 255), randint(0, 255), randint(0, 255)), box)
            final_image.paste(image, box)

        final_image.save("%s.png" % argument.name)


# Sort DIFFs by size
DIFFS.sort_by_size()
#for diff in DIFFS.items:
#    print diff.size

if DIFFS.total['width'] >= DIFFS.total['height']:
    MATRIX = DiffMatrix(width=FRAMES.items[0].image.size[0], controller=DIFFS)
else:
    MATRIX = DiffMatrix(height=FRAMES.items[0].image.size[1], controller=DIFFS)

# First frame
first_frame = ("first_frame", FRAMES.items[0].image.size[0], FRAMES.items[0].image.size[1])
MATRIX.add(first_frame)

# Add Diffs
for diff in DIFFS.items:
    block = (diff.hash, diff.width(), diff.height())
    MATRIX.add(block)
MATRIX.create_image()

#json.dumps
animation = {
    "fps": argument.fps,
    "image": "%s.png" % argument.name,
    "width": FRAMES.items[0].image.size[0],
    "height": FRAMES.items[0].image.size[1],
    #"safe_timing": True,
    "frames": []
}

for frame in FRAMES.items:
    diffs = []
    for diff in frame.diff:
        original = DIFFS.items[DIFFS.find_hash(diff[0])]
        diffs.append((diff[1],
                      diff[2],
                      original.position[0],
                      original.position[1],
                      diff[3],
                      diff[4]))
    this_frame = {
        "diff": diffs,
    }
    if frame.jump > 0:
        this_frame['jump'] = frame.jump
    animation['frames'].append(this_frame)

json = json.dumps(animation)
file = open("%s.json" % argument.name, "w")
file.write("%s = %s" % (argument.name, json))
file.close()

print "Finished!"
