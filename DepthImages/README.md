# Smart-Walker Computer Vision
Related: <https://github.com/sharare90/Smart-Walker>

## Installation
We are using Virtual Enviroments to manage our dependencies.
To install the Virtual Enviroment package, use:
`pip install virtualenv`

You can set up your Virtual Enviroment with the correct version of Python using

`virtualenv python .`

Where `python` is the command used to access Python 2.7 (required for libfreenect) on your machine, and `.` is the directory that you would like your virtual environment to be placed (leaving it as a dot places it in the root of your project).

Next, you'll want to install all required Python packages using
`pip install -r requirements.txt`

## Running
Ensure that you are connected to your virtual environment using:

`source environment_folder/bin/activate`

To begin creating test cases, create a text filed called `answers.txt` that contains a `0` on the first line. Running `python create_test.py` should handle the rest. The script captures an RGB and Depth image from a Kinect camera. You may want to throw out the first couple of images to allow time for the Kinect sensors to warm up. After saving the images, the script will ask whether or not you took an image of an obstacle, and the distance of the obstacle.

### NOTICE! There is currently a bug with create_test.py that requires you to open answers.txt to insert a new line on the first line after creating a test.

`python test_haptics.py` runs the Kinect in real time, with future haptic feedback support. Running it with the DEBUG variable set to true will result in silly print messages instead of haptic feedback. 

`python run_tests.py` will run `obstacle_detection.py` on all test cases listed in `answers.txt`. Each test requires a corresponding `test#.txt` file.
