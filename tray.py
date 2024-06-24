import multiprocessing
import os
import signal
import sys
import threading
from types import FrameType
import service
from PIL import Image, ImageDraw
from time import sleep

def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    return image

def start_tray():
    def open_web():
        print("open")

    def quit_app():
        print("quit")

    import pystray
    TrayIcon = pystray.Icon(
        "app",
        icon=create_image(64, 64, 'black', 'white'),
        menu=pystray.Menu(
            pystray.MenuItem(
                'open',
                open_web,
            ),
            pystray.MenuItem(
                'quit',
                quit_app,
            )
        )
    )
    print('initiated')
    threading.Thread(target=TrayIcon.run, daemon=True).start()

if __name__ == '__main__':
    start_tray()
    print("run")
    while True:
    #    print("run2")
    #sleep(5)
        continue
