<h1>bing wallpaper update</h1>

download and update bing wallpaper.<br/>

> supported GUI. gnome, unity, mate, cinnamon, xfce.

> not yet supported GUI. windows.

<h5>Table of Contents</h5>

- [Features](#features)
- [How to run](#how-to-run)

## Features

* download microsoft weekly bing wallpaper updates
* change background automatically

## How to run

* --download option will download bing wallpaper picutures to "~/Pictures/bing"
* --random will change pictures from "~/Pictures/bing" randomly

```bash
$ git clone https://github.com/bkit-dev/bingwallpapers.git
$ cd bingwallpapers
$ python -m venv .
$ pip install -r requirements.txt
$ python bing.py --download --random # download and change
$ python bing.py --download # downlog only
$ python bing.py --random # change only
```