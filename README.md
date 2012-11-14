#uvepe8

Video to html5 canvas

## What?

uvepe8 have two parts:

- **converter**: Receives a series of png frames and generates a final png and a json "timeline"
- **client**: A javascript script that loads that files and plays the video in a  `<canvas>` element.

## How it works

TODO (or you can look the code)

## Usage 
WIP

1) Convert your video to PNG frames, f.ex. using `ffmpeg`

```
ffmpeg -i video.mp4 -y -vcodec png test/test_%4d.png
```
**Note** It's -really- important that you number each frame as a digit of more characters than the total number of frames.

If your video have 300 frames and you use this numeration:

```
test_1.png
test_2.png
…
test_100.png
test_101.png
```
Some filesystems could read it in wrong order. I will fix this in the future but for now this is it.

2) Execute the python converter
`Example simple command here`

3) You are done!
The script have generated an `animation.json` and `animation.png` files, now you can use it with the *uvepe8 client*. [[See usage](#)]

## The animation json
```
{
    "fps": 30,
    "image": "animation.png",
    "image_class": "animation_image",
    "width": 250,
    "height": 250,
    "safe_timing": true,
    "frames": [
        {
            "diff": [
                [video_x, video_y, diff_x, diff_y, size_x, size_y],
                ["..."]
            ]
        }
    ],
    "jump": 3
}
```