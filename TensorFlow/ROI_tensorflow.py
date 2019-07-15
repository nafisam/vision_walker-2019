#!/usr/bin/env python
# coding: utf-8

##Part of the code with the detection and loading the model is taken from the tensorflow object detection python notebook on TensorFlow's github
#Imports
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.12.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.12.*.')




# ## Object detection imports
# Here are the imports from the object detection module.
from utils import label_map_util

from utils import visualization_utils as vis_util


# # Model preparation 
# ## Variables
# 
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_FROZEN_GRAPH` to point to a new .pb file.  
# 
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.
# Depending on what model you downlaod, you will have to change the model name and path_to_labels accordingly
##  depending on what model you chose: (https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)
MODEL_NAME = 'faster_rcnn_inception_resnet_v2_atrous_oid_v4_2018_12_12'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'oid_v4_label_map.pbtxt')


# ## Download Model
opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
  file_name = os.path.basename(file.name)
  if 'frozen_inference_graph.pb' in file_name:
    tar_file.extract(file, os.getcwd())


# ## Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)



# Detection
def run_inference_for_single_image(image, graph):      
    if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
    image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

    # Run inference
    output_dict = sess.run(tensor_dict,
                           feed_dict={image_tensor: np.expand_dims(image, 0)})

    # all outputs are float32 numpy arrays, so convert types as appropriate
    output_dict['num_detections'] = int(output_dict['num_detections'][0])
    output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.int64) #if using Open Images data set this should be int64
    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
    output_dict['detection_scores'] = output_dict['detection_scores'][0]
    if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
    return output_dict

#Region of Interest cordinate system
  #Anything outside of this region will not be detected
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)   
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255   
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


#Where the magic happens
import cv2
cap = cv2.VideoCapture(1) #if using built-in webcam make it 0

#Find focal length of whatever camera you are using
def distance_to_camera(knownWidth, focalLength, pixelWidth):
            return (knownWidth * focalLength) / pixelWidth
          
focal_length = 875

with detection_graph.as_default():
    with tf.Session() as sess:
        ops = tf.get_default_graph().get_operations()
        all_tensor_names = {output.name for op in ops for output in op.outputs}
        tensor_dict = {}
        for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
          ]:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
                tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
        
        #Where the video is being processed        
        while True:
            ret, image_np = cap.read()
            
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            
            # Actual detection.
            output_dict = run_inference_for_single_image(image_np, detection_graph)
            
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
              image_np,
              output_dict['detection_boxes'],
              output_dict['detection_classes'],
              output_dict['detection_scores'],
              category_index,
              instance_masks=output_dict.get('detection_masks'),
              use_normalized_coordinates=True,
              line_thickness=8)

            #Allows me to access the boxes, scores, and classes easily
            boxes = output_dict['detection_boxes']
            scores = output_dict['detection_scores']
            classes = output_dict['detection_classes']
            
            objects = []
            class_str = ""

            #finds heigh, width of video frame
            height, width, channels = image_np.shape
            print("This is width: ", width)

            #Finds the rows and columns within the video
            rows, cols = image_np.shape[:2]

            #Creates the inner left and right boundaries of the ROI
            left_boundary = [int(cols*0.30), int(rows*0.95)]
            left_boundary_top = [int(cols*0.30), int(rows*0.20)]
            right_boundary = [int(cols*0.70), int(rows*0.95)]
            right_boundary_top = [int(cols*0.70), int(rows*0.20)]

            #Outside boundaries of ROI
            bottom_left  = [int(cols*0.05), int(rows*0.95)]
            top_left     = [int(cols*0.05), int(rows*0.20)]
            bottom_right = [int(cols*0.95), int(rows*0.95)]
            top_right    = [int(cols*0.95), int(rows*0.20)]

            #Creates the ROI
            vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
            cv2.line(image_np,tuple(bottom_left),tuple(bottom_right), (255, 0, 0), 5)
            cv2.line(image_np,tuple(bottom_right),tuple(top_right), (255, 0, 0), 5)
            cv2.line(image_np,tuple(top_left),tuple(bottom_left), (255, 0, 0), 5)
            cv2.line(image_np,tuple(top_left),tuple(top_right), (255, 0, 0), 5)
            copied = np.copy(image_np)
            interested=region_of_interest(copied,vertices)
            frame_expanded = np.expand_dims(interested, axis=0)
            
            #Gets the bounded box coordinates of the detected obstacles
            ymin = int((boxes[0][0]*width))
            xmin = int((boxes[0][1]*height))
            ymax = int((boxes[0][2]*width))
            xmax = int((boxes[0][3]*height))
            Result = np.array(image_np[ymin:ymax,xmin:xmax])

            #Prints out the information on the screen
            ymin_str='y min  = %.2f '%(ymin)
            ymax_str='y max  = %.2f '%(ymax)
            xmin_str='x min  = %.2f '%(xmin)
            xmax_str='x max  = %.2f '%(xmax)
            width = xmax - xmin
            width_str='width = %.2f '%(width)
            width_inc = (xmax/75) * 3
            width_inc_str = 'width = %.2finches '%(width_inc)
           
            cv2.putText(image_np,ymin_str, (50, 30),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
            cv2.putText(image_np,ymax_str, (50, 50),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
            cv2.putText(image_np,xmin_str, (50, 70),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
            cv2.putText(image_np,xmax_str, (50, 90),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)

            print("left_boundary[0],right_boundary[0] :", left_boundary[0], right_boundary[0])
            print("left_boundary[1],right_boundary[1] :", left_boundary[1], right_boundary[1])
            print("xmin, xmax :", xmin, xmax)
            print("ymin, ymax :", ymin, ymax)

            #Goes through all the detected obstacles on the screen
            for i,b in enumerate(boxes[0]):
                if scores[i] >= 0.5:
                    #Gets the approximate distance relative to the camera
                    mid_x = (boxes[i][1]+boxes[i][3])/2
                    mid_y = (boxes[i][0]+boxes[i][2])/2
                    apx_distance = (1 - (boxes[i][3] - boxes[i][1]))**4
                    cv2.putText(image_np, '{}'.format(apx_distance), (int(mid_x*800),int(mid_y*450)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

                    #If the object is less than 60% percent away from camera and is one of the following obstacles
                      #give a verbal warnng
                    #The classes id numbers were taken from the label_amp.pbtxt
                    if apx_distance <=0.6:
                        if mid_x > 0.3 and mid_x < 0.7:
                            if classes[i] == 160:
                                os.system("say 'Door Approaching'")
                            elif classes[i] == 93:
                                 os.system("say 'Stairs Approaching'")
                            elif classes[i] == 400:
                                os.system("say 'Truck Approaching'")
                            elif classes[i] == 571:
                                os.system("say 'Car Approaching'")
                            #cv2.putText(image_np,dist_str, (400, 130),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)

            #Detects what side the object is on the ROI and tells the user to go the other way
            #Returns the distance as well - distance is shoddy and I had to do a lot of ugly math to get it within a 15% error range
            if(xmin >= left_boundary[0] and xmin != 0):
                dist = distance_to_camera(width_inc, focal_length, width)
                dist = dist *2.5
                dist_str = 'Distance = %.2finches '%(dist)
                cv2.putText(image_np,dist_str, (50, 110),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
                for i in range(3):
                    os.system("say 'Move LEFT'")
                cv2.putText(image_np,'Move LEFT!', (300, 100),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),2)
            elif(xmax <= right_boundary[0] and xmax !=0):
                dist = distance_to_camera(width_inc, focal_length, width)
                dist = dist * 2.5
                dist_str = 'Distance = %.2finches '%(dist)
                cv2.putText(image_np,dist_str, (50, 110),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
                for i in range(3): 
                    os.system("say 'Move Right'")
                cv2.putText(image_np,'Move RIGHT!', (300, 100),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),2)
            elif(xmin <= left_boundary[0] and xmax >= right_boundary[0]):
                dist = distance_to_camera(width_inc, focal_length, width)
                dist = dist *2.5
                print("Stop")
            cv2.line(image_np,tuple(left_boundary),tuple(left_boundary_top), (255, 0, 0), 5)
            cv2.line(image_np,tuple(right_boundary),tuple(right_boundary_top), (255, 0, 0), 5)

            
            cv2.imshow('object detection', cv2.resize(image_np, (800,600)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
