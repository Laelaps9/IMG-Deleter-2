import sys
import os
import cv2
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np

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

def get_config():
    global config, keyUnmark, keyMark, keyPrev, keyNext, keyStop, posX, posY, threshold
    config = []
    f = open("config", "r")
    lines = f.readlines()
    for line in lines:
        if "unmark:" in line:
            keyUnmark = line.strip(" \n")
            continue
        if "mark:" in line:
            keyMark = line.strip(" \n")
            continue
        if "previous:" in line:
            keyPrev = line.strip(" \n")
            continue
        if "next:" in line:
            keyNext = line.strip(" \n")
            continue
        if "stop:" in line:
            keyStop = line.strip(" \n")
            continue
        if "position:" in line:
            positions = line.split(":")[1].strip(" \n").split("x")
            posX = int(positions[0])
            posY = int(positions[1])
            continue
        if "comp_threshold:" in line:
            threshold = float(line.split(":")[1].strip(" \n"))

def associate_images(images, marks):
    toDelete = []
    for i, mark in enumerate(marks):
        if mark == 1:
            toDelete.append(images[i])

    delete_images(toDelete)

def compare_images(img1, img2):
    # First check if the images have the same dimensions
    if img1.shape != img2.shape:
        return -1

    # Compare images using structural similarity index
    s = ssim(img1, img2)
   
    fig = plt.figure("Comparison")
    plt.suptitle("SSIM: %.2f" % s)
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(img1, cmap = plt.cm.gray)
    plt.axis("off")

    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(img2, cmap = plt.cm.gray)
    plt.axis("off")

    plt.show()

    return s

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
    print("Normal Deletion")
    marks = [0 for i in range(len(images))]
    validFlags = ["Unmark", "Mark", "Stop", "Previous", "Next" ]
    i = 0
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    keys = {
        ord(keyUnmark[-1]): "Unmark",
        # key pressed to mark an image for deletion
        ord(keyMark[-1]): "Mark",
        # key to go back to the previous image
        ord(keyPrev[-1]):"Previous",
        # key to move on to the next image
        ord(keyNext[-1]):"Next",
        # key to stop and confirm or cancel deletion
        ord(keyStop[-1]):"Stop"
        }

    while i < len(images):
        img = cv2.imread(images[i])
        cv2.imshow("img", img)
        cv2.moveWindow("img", posX, posY)
        k = cv2.waitKey(0)
        flag = keys.get(k)
        while flag not in validFlags:
            print("Invalid option")
            print("\t" + keyUnmark) 
            print("\t" + keyMark) 
            print("\t" + keyPrev) 
            print("\t" + keyNext) 
            print("\t" + keyStop) 
            k = cv2.waitKey(0)
            flag = keys.get(k)
        
        if flag == "Mark":
            print("Marked for deletion")
            marks[i] = 1
            flag = "Next"
        elif flag == "Unmark":
            print("Unmarked for deletion")
            marks[i] = 0
            flag = "Next"
        if flag == "Next":
            if i < len(images) - 1:
                i += 1
                cv2.destroyAllWindows()
            else:
                print("Last image reached")
            continue

        if flag == "Previous":
            if i > 0:
                i -= 1
                cv2.destroyAllWindows()
            else:
                print("First image reached")
            continue
        if flag == "Stop":
            cv2.destroyAllWindows()
            break

    associate_images(images, marks)

def duplicate_deletion(images):
    for i, image in enumerate(images):
        duplicates = []
        img1 = cv2.imread(image)
        img1Gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        for image in images[i + 1:]:
            img2 = cv2.imread(image)
            img2Gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            if compare_images(img1Gray, img2Gray) >= threshold:
                duplicates.append(image)
                images.remove(image)
        if len(duplicates) > 0:
            delete_images(duplicates)

def get_deletion(option, images):
    if option == 1:
        quick_deletion(images)
    elif option == 2:
        duplicate_deletion(images)
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

get_config()
get_deletion(option, images)
