#! /usr/bin/python

import os
import numpy as np
import sys
import shutil
import pause, datetime
import keyboard


def set_n(file):
    ncommand = 'nitrogen --set-zoom-fill "{}" --head='.format(file)
    os.system(ncommand + "0")
    os.system(ncommand + "1")


def set_blck(file):
    bcommand = 'betterlockscreen -u "{}" --blur 3.0 --dim 10.0'.format(file)
    os.system(bcommand)


def set_login(pname, file):
    if pname in os.listdir():
        os.remove(os.path.join(sddm_theme_path, "assets", pname))
    shutil.copy(file, os.path.join(sddm_theme_path, "assets"))
    with open(os.path.join(sddm_theme_path, "theme.conf"), "r") as f:
        text = "\n".join(f.read().splitlines()[:-1]) + '\nBackground="{}"'.format(
            os.path.join("assets/", file.split("/")[-1])
        )
    with open(os.path.join(sddm_theme_path, "theme.conf"), "w") as f:
        f.write(text)
    with open(os.path.join(config_path, "pwall.txt"), "w") as f:
        f.write(file)


AUTO = False
hours = 0
minute = 0
seconds = 0
# home = os.path.expanduser("~")
home = "/home/sergiogd"
config_path = os.path.join(home, ".config")
sddm_theme_path = "/usr/share/sddm/themes/XeroDark/"
wall_paths = [
    os.path.join(home, "Pictures/wallpapers/desktop"),
    os.path.join(home, "Pictures/wallpapers/phone"),
]
AUTO = "a" in sys.argv
CICLE = [x for x in sys.argv[1:] if "c" in x.lower()]
with open(os.path.join(config_path, "pwall.txt"), "r") as f:
    prev_path = f.read()
pname = prev_path.split("/")[-1]
files = []
for path in wall_paths:
    files += [
        os.path.join(path, file)
        for file in os.listdir(path)
        if (".jpg" in file or ".png" in file)
    ]
np.random.shuffle(files)
if "y" in sys.argv:
    login = True
elif "n" in sys.argv:
    login = False
else:
    login = input("update login y/[n]").lower() == "y"
if len(CICLE) > 0:
    i = 0
    while True:
        dt = datetime.datetime.now()
        dt += datetime.timedelta(seconds=int(CICLE[-1][1:]))
        file = files[i]
        print(
            "Setting Wallpaper to: " + file + "| Next at: " + dt.strftime("%H:%M:%S"),
        )
        set_n(file)

        set_blck(file)

        if login:
            set_login(pname, file)
        pause.until(dt)
        i = (1 + i) % len(files)
else:
    i = 0
    while True:
        file = files[i]
        print(file)
        set_n(file)
        option = input("Keep: ").lower()
        if AUTO or option == "y":
            break
        elif option == "p":
            i = (i - 1) % len(files)
        else:
            i = (1 + i) % len(files)
    set_blck(file)

    if login:
        set_login(pname, file)
