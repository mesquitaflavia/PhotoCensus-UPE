"""
test_kit.py - Checks whether the PhotoCensus kit is working.
Usage:  python test_kit.py
"""
from black_box import *

print("1) Folders and photos")
show_folders()

print("\n2) Module 1 functions")
photo = photo_name("office", 1)
print("   photo:", photo)
print("   count_objects(photo)              =", count_objects(photo))
print("   count_class(photo, 'keyboard')    =", count_class(photo, "keyboard"))
print("   main_object(photo)                =", main_object(photo))
print("   max_confidence(photo)             =", max_confidence(photo))

print("\n3) Module 2 functions")
print("   list_folders()         =", list_folders())
print("   list_photos('street')  =", list_photos("street")[:2], "...")
print("   detect(photo)          =", detect(photo))

print("\n4) Full AI mode (for new photos)")
try:
    import ultralytics  # noqa: F401
    print("   ultralytics installed: new photos can be analyzed.")
except ImportError:
    print("   ultralytics NOT installed: only the kit photos can be used.")
    print("   (This is enough for the project. For new photos, run the installer.)")

print("\nKit OK.")
