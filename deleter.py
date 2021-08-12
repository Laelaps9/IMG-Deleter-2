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
        if ".png" in file or ".jpg" in file:
            images.append(os.path.join(path, file))
    return images

def define_keys(skip, delete, prevImg, nextImg, stop):
    global switch 
    switch = {
            # represents images to skip
            ord(skip): "Skip",
            # represents images marked for deletion
            ord(delete): "Delete",
            #
            ord(prevImg):"Previous Image",
            #
            ord(nextImg):"Next Image",
            #
            ord(stop):"Stop"
            }

def get_keys():
    global config, keySkip, keyDelete, keyPrev, keyNext, keyStop
    config = []
    f = open("keys.conf", "r")
    lines = f.readlines()
    for line in lines:
        if "skip:" in line:
            keySkip = line
            skip = line.split(":")[1].strip(" \n")
            continue
        if "delete:" in line:
            keyDelete = line
            delete = line.split(":")[1].strip(" \n")
            continue
        if "previous:" in line:
            prevImg = line.split(":")[1].strip(" \n")
            continue
        if "next:" in line:
            nextImg = line.split(":")[1].strip(" \n")
            continue
        if "stop:" in line:
            stop = line.split(":")[1].strip(" \n")
    
    define_keys(skip, delete, prevImg, nextImg, stop)

def delete_images(images):
    print("\nImages to be deleted:")
    for image in images:
        print(image)

    proceed = input("Are you sure you want to proceed? (y/n): ")
    if proceed == "y" or proceed == "yes":
        print("Deleting...")
        for image in images:
            os.remove(image)

        print("Complete")
        return

    print("Cancelled")

def quick_deletion(images):
    print("Quick Deletion")
    # Array that will specify which images are deleted
    toDelete = []
    for i, image in enumerate(images):
        img = cv2.imread(image)
        cv2.imshow(image, img)
        k = cv2.waitKey(0)
        flag = switch.get(k)
        while flag != "Skip" and flag != "Delete":
            print("Invalid option")
            print("\t" + keySkip, "\t" + keyDelete)
            k = cv2.waitKey(0)
            flag = switch.get(k)
        
        cv2.destroyAllWindows()
        if flag == "Delete":
            print("Delete")
            toDelete.append(image)
            continue

        print("Skip")

    delete_images(toDelete)

def duplicate_deletion():
    print("Duplicate Deletion")

def get_deletion(option, images):
    if option == 1:
        quick_deletion(images)
    elif option == 2:
        duplicate_deletion()
    else:
        print_help("Invalid Option")

args = sys.argv[1:]

# If no arguments were given, call get_dir()
if len(args) == 0:
    path = input("Input the path to the directory (e.g. /home/user/Pictures): ")
else:
    if len(args) > 1:
        print_help("Too many arguments")
    
    path = args[0]

images = get_images(path)

option = int(input("""
Select a deletion mode (number):
1. Quick Deletion
2. Duplicate Deletion
"""))

get_keys()
get_deletion(option, images)
