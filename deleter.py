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

def define_keys(unmark, mark, prevImg, nextImg, stop):
    global switch 
    switch = {
            ord(unmark): "Unmark",
            # key pressed to mark an image for deletion
            ord(mark): "Mark",
            # key to go back to the previous image
            ord(prevImg):"Previous",
            # key to move on to the next image
            ord(nextImg):"Next",
            # key to stop and confirm or cancel deletion
            ord(stop):"Stop"
            }

def get_config():
    global config, keyUnmark, keyMark, keyPrev, keyNext, keyStop, posX, posY
    config = []
    f = open("config", "r")
    lines = f.readlines()
    for line in lines:
        if "unmark:" in line:
            keyUnmark = line
            unmark = line.split(":")[1].strip(" \n")
            continue
        if "mark:" in line:
            keyMark = line
            mark = line.split(":")[1].strip(" \n")
            continue
        if "previous:" in line:
            keyPrev = line
            prevImg = line.split(":")[1].strip(" \n")
            continue
        if "next:" in line:
            keyNext = line
            nextImg = line.split(":")[1].strip(" \n")
            continue
        if "stop:" in line:
            keyStop = line
            stop = line.split(":")[1].strip(" \n")
            continue
        if "position:" in line:
            positions = line.split(":")[1].strip(" \n").split("x")
            posX = int(positions[0])
            posY = int(positions[1])
    
    define_keys(unmark, mark, prevImg, nextImg, stop)

def associate_images(images, marks):
    toDelete = []
    for i, mark in enumerate(marks):
        if mark == 1:
            toDelete.append(images[i])

    delete_images(toDelete)

def delete_images(images):
    print("\nImages to be deleted (" + str(len(images)) + "):")
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
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    validFlags = ["Unmark", "Mark", "Stop"]
    for image in images:
        img = cv2.imread(image)
        cv2.imshow("img", img)
        cv2.moveWindow("img", posX, posY)
        k = cv2.waitKey(0)
        flag = switch.get(k)
        while flag not in validFlags:
            print("Invalid option")
            print("\t" + keyUnmark, 
                  "\t" + keyMark, 
                  "\t" + keyStop)
            k = cv2.waitKey(0)
            flag = switch.get(k)
        
        cv2.destroyAllWindows()
        if flag == "Delete":
            print("Marked for deletion")
            toDelete.append(image)
            continue
        if flag == "Stop":
            break

        print("Skip")

    delete_images(toDelete)

def normal_deletion(images):
    print("Normal Deletion")
    marks = [0 for i in range(len(images))]
    validFlags = ["Unmark", "Mark", "Stop", "Previous", "Next" ]
    i = 0
    while i < len(images):
        img = cv2.imread(images[i])
        cv2.imshow("img", img)
        k = cv2.waitKey(0)
        flag = switch.get(k)
        while flag not in validFlags:
            print("Invalid option")
            print("\t" + keyUnmark, 
                  "\t" + keyMark, 
                  "\t" + keyPrev, 
                  "\t" + keyNext, 
                  "\t" + keyStop)
            k = cv2.waitKey(0)
            flag = switch.get(k)

        if flag == "Unmark":
            print("Unmarked for deletion")
            marks[i] = 0
            continue
        if flag == "Mark":
            print("Marked for deletion")
            marks[i] = 1
            continue
        if flag == "Previous":
            if i > 0:
                i -= 1
                cv2.destroyAllWindows()
            else:
                print("First image reached")
            continue
        if flag == "Next":
            if i < len(images) - 1:
                i += 1
                cv2.destroyAllWindows()
            else:
                print("Last image reached")
            continue
        if flag == "Stop":
            cv2.destroyAllWindows()
            break

    associate_images(images, marks)

def duplicate_deletion():
    print("Duplicate Deletion")

def get_deletion(option, images):
    if option == 1:
        quick_deletion(images)
    elif option == 2:
        normal_deletion(images)
    elif option == 3:
        duplicate_deletion
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
2. Normal Deletion
3. Duplicate Deletion
"""))

get_config()
get_deletion(option, images)
