"""
example_module2.py - How to CALL the Module 2 functions.
This is not the project solution: it is only a starting point.
"""
from black_box import *

print("Folders:", list_folders())

photos = list_photos("kitchen")
first = photos[0]
detections = detect(first)      # list of tuples (class_name, confidence)
print("Detections in", first, "->", detections)

for class_name, confidence in detections:
    print(f"  {class_name:<15} {confidence:.0%}")
