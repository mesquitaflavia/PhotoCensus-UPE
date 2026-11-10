"""
example_module1.py - How to CALL the Module 1 functions.
This is not the project solution: it is only a starting point.
"""
from black_box import *

folder = "street"
amount = total_photos(folder)
print(f"Folder '{folder}' has {amount} photos.")

for number in range(1, amount + 1):
    photo = photo_name(folder, number)
    objects = count_objects(photo, 0.5)
    cars = count_class(photo, "car", 0.5)
    print(f"Photo {number}: {objects} object(s), {cars} car(s)")
