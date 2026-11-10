"""
=====================================================================
 black_box.py  -  PhotoCensus Project
=====================================================================

 DO NOT MODIFY THIS FILE. You only need to IMPORT it and CALL the
 functions below. You do not need to understand how it works inside.

 This file stays in /kit. Your code goes in /groups/group_XX/
 (see "How to import from your group folder" below).

 ------------------------------------------------------------------
 MODULE 1 FUNCTIONS  (return only simple values: int, float, str, bool)
 ------------------------------------------------------------------
   folder_exists(folder)                          -> bool
   total_photos(folder)                           -> int
   photo_name(folder, number)                     -> str   (number starts at 1)
   count_objects(photo, min_confidence)           -> int
   count_class(photo, class_name, min_confidence) -> int
   main_object(photo)                             -> str   ("" if nothing found)
   max_confidence(photo)                          -> float (0.0 if nothing found)
   show_folders()                                 -> None  (only prints)
   show_classes()                                 -> None  (only prints)

 ------------------------------------------------------------------
 MODULE 2 FUNCTIONS  (return data structures)
 ------------------------------------------------------------------
   list_folders()       -> list[str]                e.g. ["animals", "kitchen", ...]
   list_photos(folder)  -> list[str]                e.g. ["images/street/street_01.jpg", ...]
   detect(photo)        -> list[tuple[str, float]]  e.g. [("car", 0.91), ("person", 0.48)]

 Notes
   - "folder" is the NAME of a folder inside images/ (e.g. "street").
     For your own photos (optional), it can also be a path to a folder
     inside your group directory (e.g. "my_photos").
   - "photo" is the path returned by photo_name() or list_photos().
     The file name alone also works (e.g. "street_01.jpg").
   - "confidence" goes from 0.0 to 1.0: the higher, the more "certain"
     the model is.
   - The photos in this kit were already analyzed by the YOLO model, so
     the kit works WITHOUT INSTALLING ANYTHING. To analyze your own new
     photos, run the installer first (install_windows.bat or
     install_linux_mac.sh).

 How to import from your group folder (/groups/group_XX/main.py):

     import os, sys
     sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "kit"))
     from black_box import *
=====================================================================
"""

import json as _json
import os as _os

_BASE = _os.path.dirname(_os.path.abspath(__file__))
_IMAGES_DIR = _os.path.join(_BASE, "images")
_CACHE_FILE = _os.path.join(_BASE, "data", "detections.json")
_CLASSES_FILE = _os.path.join(_BASE, "data", "classes.json")
_MODEL_FILE = _os.path.join(_BASE, "data", "yolov8n.pt")
_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
_MODEL_MIN_CONFIDENCE = 0.25

_cache = None
_classes = None
_model = None


# ===================================================================
# Internal functions (do not call them directly)
# ===================================================================
def _load_data():
    global _cache, _classes
    if _cache is None:
        with open(_CACHE_FILE, encoding="utf-8") as file:
            _cache = _json.load(file)
        with open(_CLASSES_FILE, encoding="utf-8") as file:
            _classes = _json.load(file)


def _real_path(photo):
    """Accepts a full path, a relative path or only the file name."""
    photo = str(photo).strip()
    if _os.path.isfile(photo):
        return photo
    candidate = _os.path.join(_BASE, photo)
    if _os.path.isfile(candidate):
        return candidate
    name = _os.path.basename(photo)
    for folder in sorted(_os.listdir(_IMAGES_DIR)):
        candidate = _os.path.join(_IMAGES_DIR, folder, name)
        if _os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError(
        f"[black_box] Photo not found: '{photo}'. "
        "Use the path returned by photo_name() or list_photos()."
    )


def _detect_with_model(path):
    global _model
    try:
        from ultralytics import YOLO
    except ImportError:
        raise RuntimeError(
            "[black_box] This photo is not part of the original kit and the AI "
            "library is not installed. Run the installer (install_windows.bat or "
            "install_linux_mac.sh) and try again."
        )
    if _model is None:
        print("[black_box] Loading the AI model (first time only)...")
        _model = YOLO(_MODEL_FILE if _os.path.isfile(_MODEL_FILE) else "yolov8n.pt")
    output = _model(path, verbose=False, conf=_MODEL_MIN_CONFIDENCE)[0]
    result = []
    for box in output.boxes:
        result.append([_model.names[int(box.cls)], round(float(box.conf), 2)])
    return result


def _detections(photo):
    _load_data()
    path = _real_path(photo)
    name = _os.path.basename(path)
    record = _cache.get(name)
    if record is None or record["bytes"] != _os.path.getsize(path):
        record = {"bytes": _os.path.getsize(path), "detections": _detect_with_model(path)}
        _cache[name] = record  # keep in memory to avoid running the model again
    return record["detections"]


def _folder_path(folder):
    """Kit folder name (e.g. "street") or a path to your own photo folder."""
    name = str(folder).strip()
    kit_path = _os.path.join(_IMAGES_DIR, name.lower())
    if name and _os.path.isdir(kit_path):
        return kit_path
    if name and _os.path.isdir(name):
        return _os.path.abspath(name)
    return kit_path


def _folder_photos(folder):
    path = _folder_path(folder)
    if not _os.path.isdir(path):
        raise FileNotFoundError(
            f"[black_box] Folder '{folder}' does not exist. Use show_folders() to see the options."
        )
    names = sorted(n for n in _os.listdir(path) if n.lower().endswith(_EXTENSIONS))
    if _os.path.dirname(path) == _IMAGES_DIR:
        return [_os.path.join("images", _os.path.basename(path), n) for n in names]
    return [_os.path.join(path, n) for n in names]


# ===================================================================
# MODULE 1 - simple values
# ===================================================================
def folder_exists(folder):
    """True if images/<folder> exists. Useful to validate input with while."""
    return _os.path.isdir(_folder_path(folder))


def total_photos(folder):
    """Number of photos inside images/<folder>."""
    return len(_folder_photos(folder))


def photo_name(folder, number):
    """Path of photo number 'number' (1, 2, 3, ...) of the folder."""
    photos = _folder_photos(folder)
    number = int(number)
    if number < 1 or number > len(photos):
        raise IndexError(
            f"[black_box] Folder '{folder}' has photos 1 to {len(photos)}; received {number}."
        )
    return photos[number - 1]


def count_objects(photo, min_confidence=0.5):
    """How many objects (of any class) were detected with confidence >= min_confidence."""
    total = 0
    for _name, conf in _detections(photo):
        if conf >= min_confidence:
            total += 1
    return total


def count_class(photo, class_name, min_confidence=0.5):
    """How many objects of 'class_name' (e.g. "person") are in the photo, with confidence >= min_confidence."""
    class_name = str(class_name).strip().lower()
    total = 0
    for name, conf in _detections(photo):
        if name == class_name and conf >= min_confidence:
            total += 1
    return total


def main_object(photo):
    """Class of the object with the HIGHEST confidence in the photo. Returns "" if nothing was detected."""
    best, best_conf = "", -1.0
    for name, conf in _detections(photo):
        if conf > best_conf:
            best, best_conf = name, conf
    return best


def max_confidence(photo):
    """Highest confidence found in the photo (0.0 if nothing was detected)."""
    highest = 0.0
    for _name, conf in _detections(photo):
        if conf > highest:
            highest = conf
    return highest


def show_folders():
    """Prints the available photo folders and how many photos each one has."""
    print("Folders available in images/:")
    for folder in sorted(_os.listdir(_IMAGES_DIR)):
        if _os.path.isdir(_os.path.join(_IMAGES_DIR, folder)):
            print(f"  - {folder:<12} ({total_photos(folder)} photos)")


def show_classes():
    """Prints all class names the model can recognize."""
    _load_data()
    names = sorted(_classes)
    print(f"The model recognizes {len(names)} classes:")
    line = "  "
    for name in names:
        if len(line) + len(name) > 76:
            print(line)
            line = "  "
        line += name + ", "
    print(line.rstrip(", "))


# ===================================================================
# MODULE 2 - data structures
# ===================================================================
def list_folders():
    """List with the names of the folders inside images/."""
    return sorted(f for f in _os.listdir(_IMAGES_DIR)
                  if _os.path.isdir(_os.path.join(_IMAGES_DIR, f)))


def list_photos(folder):
    """List with the paths of all photos in images/<folder>."""
    return _folder_photos(folder)


def detect(photo):
    """
    List of tuples (class_name, confidence) with ALL objects detected in the
    photo (confidence from 0.25). Filtering by confidence is your job.
    """
    result = []
    for name, conf in _detections(photo):
        result.append((name, conf))
    return result


# ===================================================================
# Quick test:  python black_box.py
# ===================================================================
if __name__ == "__main__":
    show_folders()
    photo = photo_name("street", 1)
    print("\nExample with", photo)
    print("  count_objects ->", count_objects(photo))
    print("  count_class   ->", count_class(photo, "car"), "car(s)")
    print("  main_object   ->", main_object(photo))
    print("  detect        ->", detect(photo))
