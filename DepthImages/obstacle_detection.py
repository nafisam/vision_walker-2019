import numpy as np

DEBUG = True
# input - Depth image.
# width - Determines where we pick the y2/x2 for the slope calculation.
# threshold - Max detection distance.
def detect(input, width, threshold):
    array = input

    # Only required if we're not averageing the array by this point.
    # Gets the 640 x 480 array and turns it into a 1-d array, using the middle value instead of the average
    if len(np.shape(array)) > 1:
        h, w = np.shape(array)
        array = array[:, w / 2]

    # Remove 0s, as they are error values.
    array = array[array != 0]

    # For now we assume super close object mostly filling screen = bad.
    # The following 2 lines return 1 if there are too many error states in the array, 1 means nothing happens in test_haptics 
    # so if we want to be over cautious we should probably make far away buzz
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
        y1 = array[index]
        y2 = array[index + width]

        slope = (y2 - y1) / width

        index += width	# why are we doing this? it skips <width> points, is it just to be faster? operating under the assumption that any points between those we're comparing would yield similar results?

        # Break out of the loop if we have a non-positive slope.
	# This is the case of a regular obstacle
        if slope < -2:
            break
        
	# This is the case of a drop-off, ie stairs, curb, etc.
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
        y1 = array[index]
        y2 = array[index + width]

        slope = (y2 - y1) / width

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
