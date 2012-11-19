#uvepe8

Video to html5 canvas

## What?

uvepe8 have two parts:

- **converter**: Receive a series of png frames and generates a final png and a json "timeline".
- **player**: A javascript script that loads that files and plays the video in a  `<canvas>` element.

This is initially intented for presentations or screen captures, but with the proper algorithms could be used even for short videos. 

Remember, still working on it.

## How it works

#### The converter
The converters look in the frames of the video for differences, based on the selected algorithm (see [Algorithms](#TODO)). It's output is a PNG file with the original frame and all the differences between the rest of the frames.
Also a JSON file that contains the timeline info (every frame that needs to be drawn).

### The player


## Quick usage

1) Convert your video to PNG frames, f.ex. using `ffmpeg`

```
ffmpeg -i video.mp4 -y -vcodec png frames/%6d.png
```

**Note** It's -really- important that you number each frame as a digit of more characters than the total number of frames. Some filesystems could read it in wrong order. I will fix this in the future but for now this is it.

2) Execute the python converter 

```
python uvepe8.py frames my_animation
```

3) You are almost done!
The script have generated an `my_animation.json` and `my_animation.png` files, now you can use it with the *uvepe8 client*.

For por information on the converter, `python uvepe8.py -h` or look at the code

4) Edit your HTML and include Zepto or jQuery on your code.

5) Include the uvepe8 player and your animation json.

```
<script src="uvepe8.js"></script>
<script src="my_animation.json"></script>
```

6) Create a container where you want the video

```
<div id="uvepe8_video"></div>
```

7) Include the player. The first argument is the element where the video will embed, the second is the animation timeline name you specified in the converter script. There's an optional third parameter for autoplay the video, defaults to *true*.

```
window.onload = function() {
	player = uvepe8.player("#uvepe8_video", my_animation)
}
```

## The animation json

```
my_animation = {
    "fps": 30,
    "image": "animation.png",
    "image_class": "animation_image",
    "width": 250,
    "height": 250,
    "safe_timing": true,
    "frames": [
        {
	        "jump": 3,
            "diff": [
                [video_x, video_y, diff_x, diff_y, size_x, size_y],
                ["..."]
            ]
        }
    ]
}
```

## Compressing the PNG

Compressing the final PNG has to be done manually at the moment. It's done via `pngcrush` ([info](http://pmt.sourceforge.net/pngcrush/)), and if you don't wan't to read the docs, can start with this simple line:

```
pngcrush -rem gAMA -rem cHRM -rem iCCP -rem sRGB origial_file.png destination_file.png
```

# TODO

- Dont require libraries. Be standalone.
- Complete the docs and comment the code ^_^U
- Information of the algorithms and how to create your own.
- Read the files in order even if the files are not named propertly.
- Cleanup of the diff object - diff controller - diffmatrix.
- Animation fallback to DIVs for IE<9
- Performance check on browsers
- Order files and code on the main file
- Integrate [pngcrush](http://pmt.sourceforge.net/pngcrush/)
- Minimal percentage to count as difference