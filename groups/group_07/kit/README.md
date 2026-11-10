# PhotoCensus: student kit

PhotoCensus is a console system that takes a "census" of the objects that appear in photos: how many people, cars, chairs, dogs etc. there are in each image, in each folder and in the whole collection.

Object detection is done by an Artificial Intelligence model (YOLO) used as a black box. You do not need to understand how the AI works. You only call the functions in `black_box.py`.

## Kit contents

```
kit/
├── black_box.py            <- DO NOT MODIFY. Functions you will call
├── test_kit.py             <- run this first to check that everything works
├── example_module1.py      <- example calls for the Module 1 functions
├── example_module2.py      <- example calls for the Module 2 functions
├── install.py              <- AI installer (optional, only for new photos)
├── install_windows.bat     <- installer shortcut for Windows
├── install_linux_mac.sh    <- installer shortcut for Linux/macOS
├── IMAGE_CREDITS.txt       <- source and license of each photo
├── data/                   <- DO NOT MODIFY. AI results and model
└── images/                 <- 48 photos in 6 folders (8 photos each)
    ├── animals/      animals_01.jpg ... animals_08.jpg
    ├── kitchen/      kitchen_01.jpg ... kitchen_08.jpg
    ├── living_room/  living_room_01.jpg ... living_room_08.jpg
    ├── office/       office_01.jpg ... office_08.jpg
    ├── sports/       sports_01.jpg ... sports_08.jpg
    └── street/       street_01.jpg ... street_08.jpg
```

## Getting started

This kit lives in the `/kit` folder of the central repository and comes automatically with your fork. **Do not copy it and do not modify it.** Your group's code goes only in `/groups/group_XX/`.

1. From the repository root, run `python kit/test_kit.py`. If it prints "Kit OK.", you are ready.
2. Copy the template `/groups/group_00/` to `/groups/group_XX/` (XX = your group number).
3. Write your code in `/groups/group_XX/main.py`. The first lines must be:

```python
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "kit"))
from black_box import *
```

These lines let your code find `black_box.py` in `/kit`, no matter which folder you run it from.

You do not need to install anything to use the 48 kit photos: the AI results are already stored in `data/detections.json`. You only need Python 3.9 or newer.

We recommend (but do not require) writing your own code in English, like this kit (file names, variables, functions and comments). Code in Portuguese is also accepted.

## Available functions

### Module 1: simple values only

| Function | Returns | Example |
|---|---|---|
| `folder_exists(folder)` | `bool` | `folder_exists("street")` → `True` |
| `total_photos(folder)` | `int` | `total_photos("street")` → `8` |
| `photo_name(folder, number)` | `str` | `photo_name("street", 1)` → `"images/street/street_01.jpg"` |
| `count_objects(photo, min_confidence)` | `int` | `count_objects(photo, 0.5)` → `4` |
| `count_class(photo, class_name, min_confidence)` | `int` | `count_class(photo, "car", 0.5)` → `2` |
| `main_object(photo)` | `str` | `main_object(photo)` → `"traffic light"` |
| `max_confidence(photo)` | `float` | `max_confidence(photo)` → `0.75` |
| `show_folders()` | prints only | lists the folders and how many photos each has |
| `show_classes()` | prints only | lists the 80 classes the AI recognizes |

Photo numbers start at 1. If `min_confidence` is omitted, `0.5` is used.

### Module 2: data structures

| Function | Returns | Example |
|---|---|---|
| `list_folders()` | `list[str]` | `["animals", "kitchen", ...]` |
| `list_photos(folder)` | `list[str]` | `["images/street/street_01.jpg", ...]` |
| `detect(photo)` | `list[tuple[str, float]]` | `[("car", 0.70), ("person", 0.41)]` |

`detect` returns all objects with confidence from 0.25. Filtering by the minimum confidence is your job.

## Classes found in the kit photos

airplane, bicycle, book, bottle, bowl, bus, cake, car, cat, chair, couch, cup, dining table, dog, elephant, frisbee, giraffe, horse, keyboard, knife, laptop, microwave, motorcycle, mouse, oven, person, potted plant, refrigerator, remote, sink, skateboard, sports ball, stop sign, suitcase, surfboard, tennis racket, traffic light, train, truck, tv, vase, zebra

Names are in lowercase, exactly as written above.

Like any AI, the model sometimes makes mistakes. For example, it may see an "airplane" in a kitchen. This is expected and should not be fixed in the code. Using the minimum confidence to filter out these mistakes is part of the project.

## New photos (optional)

To analyze photos taken by your group:

1. Run the installer once. On Windows, double-click `kit/install_windows.bat`. On Linux or macOS, run `bash kit/install_linux_mac.sh`. The installer needs internet access and downloads about 1 GB.
2. Put the photos in a folder **inside your group directory**, for example `/groups/group_XX/my_photos/`. Never add photos to `/kit/images/`.
3. Pass the folder path to the usual functions:

```python
GROUP_DIR = os.path.dirname(os.path.abspath(__file__))
my_folder = os.path.join(GROUP_DIR, "my_photos")
photos = list_photos(my_folder)
```

For the first new photo, the AI takes a few seconds to load.

During the presentation, the professor will use the original kit photos for the quick tests.
