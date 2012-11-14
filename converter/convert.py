from controller import FrameController, DiffController
#from diff_methods import *
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

# Export as animation in keynote. Quicktime Lossless RGBA
# Conversion: ffmpeg -i animation.mov -y -vcodec png -pix_fmt rgba test/test_%4d.png

# Javascript set timeout:
# DELAY TIMING
# Put setTimeout before exec any code, so timing will be more accurate

# Globals
# Original video FPS
FPS = 30 # Delay timing = 60*1000/FPS miliseconds

FRAMES = FrameController()
DIFFS = DiffController()

DIR = '../test/'
FILETYPE = 'png'
FILES = glob.glob("%s*.%s" % (DIR, FILETYPE))

WIDTH = 250 # TODO
HEIGHT = WIDTH # TODO

ANIMATION = {
    "fps": FPS,
    "image": None,
    "width": WIDTH,
    "height": HEIGHT
}

TOTAL_FILES = len(FILES)
CURRENT_FILE = 1
echo("%10s %8s " % ("FRAMES", "DIFFS"))
for file in FILES:
    if FRAMES.current is -1:
        # First frame is just original one
        FRAMES.append(file)
    else:
        # Checking for diffs. Bitches LOVE diffs
        FRAMES.append(file)
        diffs = FRAMES.get_current().get_difference()
        if not diffs:
            FRAMES.get_previous().jump += 1
            FRAMES.remove(FRAMES.get_current())
        else:
            for diff in diffs:
                diff_number = DIFFS.find_hash(diff['hash'])
                if diff_number is None:
                    DIFFS.append(diff)
                    diff_number = DIFFS.current
                FRAMES.get_current().diff.append(diff_number)
    echo("%10s %8s Processing..." % ("%d/%d" % (CURRENT_FILE, TOTAL_FILES), len(DIFFS.items)), True, False)
    CURRENT_FILE += 1

print ""
print "-- Summary --"
print "Total frames: %d" % TOTAL_FILES
print "Total frames saved: %d" % len(FRAMES.items)
print "Total diffs saved: %d" % len(DIFFS.items)
print ""

#print FRAMES.items


