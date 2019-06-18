import numpy as np

DEBUG = True
# input - Depth image.
# width - Determines where we pick the y2/x2 for the slope calculation.
# threshold - Max detection distance.
def detect(input, width, threshold):
    array = input

    # Only required if we're not averageing the array by this point.
    # Gets the 640 x 480 array and turns it into a 1-d array across the middle.
    if len(np.shape(array)) > 1:
        h, w = np.shape(array)
        array = array[:, w / 2]

    # Remove 0s, as they are error values.
    array = array[array != 0]

    # For now we assume super close object mostly filling screen = bad.
    if len(array) < 200:
        return 1

    # Flip the array so that we have it in a more intuitive order.
    # array = array[::-1]

    # Index, used to keep track of where we break out of the while loop.
    index = 0

    # Current closest distance, updated if we break out of the 1st while loop.
    distance = 9999

    while index < len(array) - width:
        # Slope calculation
        x1 = index
        y1 = array[index]
        x2 = index + width
        y2 = array[index + width]

        slope = (y2 - y1) / (x2 - x1)

        index += width

        # Break out of the loop if we have a non-positive slope.
        if slope < -2:
            break
        
        if slope > 200:
            return y1

    # Continue where we left off from ^
    # Find the lowest y-value, corresponding to the closest point.
    while index < len(array):
        if array[index] < distance:
            distance = array[index]
        index += 1
    if DEBUG:
	    print("Debug distance is {}".format(distance))
    # We've found an object if the distance is less than our threshold.
    if distance > threshold:
        return -1  # NO OBJECT DETECTED
    else:
        return distance  # OBJECT DETECTED


# Same as above, but we read the depth image from a file
def detect_file(input_file, width, threshold):
##    array = np.loadtxt(input_file)
    array = input_file

    if len(np.shape(array)) > 1:
        h, w = np.shape(array)
        array = array[:, w / 2]

    array = array[array != 0]

    if len(array) < 200:
        return 1

    #array = array[::-1]

    index = 0

    distance = 9999

    while index < len(array) - width:
        x1 = index
        y1 = array[index]
        x2 = index + width
        y2 = array[index + width]

        slope = (y2 - y1) / (x2 - x1)

        index += width

        if slope < -2:
            break
        
        if slope > 200:
            return y1

    while index < len(array):
        if array[index] < distance:
            distance = array[index]
        index += 1

    print(distance)
    if distance > threshold:
        return -1  # NO OBJECT DETECTED
    else:
        return distance  # OBJECT DETECTED
