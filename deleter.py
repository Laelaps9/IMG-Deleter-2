import sys
import os
import cv2

def print_help(msg):
    print("\n" + msg)
    print("""
Usage: python3 deleter.py [argument]
    
Arguments:
    <path>               Use this path in the program
    -h or --help         Print Help (this message) and exit
    """)
    quit()

def get_images(path):
    files = os.listdir(path)
    images = []
    for file in files:
        if (".png" in file or ".jpg" in file):
            images.append(file)
    return images

def simple_deletion(path, images):
    print("Simple Deletion")
    for name in images:
        fullPath = os.path.join(path, name)
        print(fullPath)
        img = cv2.imread(fullPath)
        cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def duplicate_deletion():
    print("Duplicate Deletion")

def get_deletion(option, path, images):
    if(option == 1):
        simple_deletion(path, images)
    elif(option == 2):
        print("Option 2")
        duplicate_deletion()
    else:
        print_help("Invalid Option")

args = sys.argv[1:]

# If no arguments were given, call get_dir()
if(len(args) == 0):
    path = input("Input the path to the directory (e.g. /home/user/Pictures): ")
else:
    if(len(args) > 1):
        print_help("Too many arguments")
    path = args[0]

images = get_images(path)

option = int(input("""
Select a deletion mode (number):
1. Simple deletion
2. Duplicate deletion
"""))

get_deletion(option, path, images)

#os.remove(test)
