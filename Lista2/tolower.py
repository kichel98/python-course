import sys
import os


for root, subdirs, files in os.walk(sys.argv[1]):
    for subdir in subdirs:
        os.rename(os.path.join(root, subdir), os.path.join(root, subdir.lower()))
    for file in files:
        os.rename(os.path.join(root, file), os.path.join(root, file.lower()))
