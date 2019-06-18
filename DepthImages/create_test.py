# import the necessary modules
import freenect
import numpy as np
import sys
import time
import math
from scipy.misc import imshow
from PIL.Image import fromarray


# NOTE THIS IS CURRENTLY BUGGED DUE TO THE FIRST LINE BEING
# PRINTED INCORRECTLY IN ANSWERS.TXT

def get_video():
    array, _ = freenect.sync_get_video()
    return array

def get_depth():
    array, _ = freenect.sync_get_depth()
    return array

def get_depth_mm():
    array,_ = freenect.sync_get_depth(format=freenect.DEPTH_MM)
    return array


if __name__ == "__main__":
    while 1:
        keep_images = "n"
        while keep_images != "y":
            # Get a frame from RGB camera & depth sensor
            array = get_depth()
            print(array)
            depth = array.astype(np.uint8)
           # print "depth = ", depth
            # Pillow doesn't like mm depths, but we need it anyways
            depth_mm = get_depth_mm()
            print(depth_mm)
            color = get_video()
            
            keep_images = raw_input("Do you wish to keep these images? (y/n): ")

        # Get the test number we're going to create
        with open("answers.txt") as ans:
            answers = ans.readlines()
        ans.close()

        answers[0] = str(int(answers[0]) + 1)
        test_count = int(answers[0])

        # Create output files
        f = open("test" + str(test_count) + '.txt', 'w')
        h, w = np.shape(array)
        line = ""

        for py in range(0, h):  # height
            for px in range(0, w):  # widths
                line += str(depth_mm[py][px]) + " "
            f.write(line + "\n\n")
            line = ""
        f.close()

        color_img = fromarray(color)
        color_img.save('test{}color.png'.format(test_count))
		
        depth_img = fromarray(depth)
        depth_img.save('test{}depth.png'.format(test_count))

        is_obstacle = raw_input("Is there an obstacle present? (True/False): ")
        distance = raw_input("Please input the distance of the object in mm (any if there is none): ")

        answers.append("\n\n{} {}".format(is_obstacle, str(distance)))

        with open("answers.txt", 'w') as ans:
            ans.writelines(answers)
        ans.close()
