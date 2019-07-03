


import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import time
import numpy as np
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
import matplotlib.pyplot as plt
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


# This is needed to display the images if you are running from python notebook.
get_ipython().run_line_magic('matplotlib', 'inline')

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")


# What model to download
#make sure model is downloaded from tensorflow github page and unzipped
MODEL_NAME = 'ssd_mobilenet_v1_0.75_depth_300x300_coco14_sync_2018_07_03'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/research/object_detection/'
CWD_PATH = os.getcwd()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(CWD_PATH, 'data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

#Creates label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


#Creates a region of interest, so if an object shows up in this region then the user is alerted
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)   
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (300,) * channel_count
    else:
        ignore_mask_color = 300   
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


#Takes live video
cap=cv2.VideoCapture(0) # 0 stands for very first webcam attach
filename="test.avi"
codec=cv2.VideoWriter_fourcc('m','p','4','v')#fourcc stands for four character code
framerate=30
resolution=(640,480)
    
VideoFileOutput=cv2.VideoWriter(filename,codec,framerate, resolution)

def distance_to_camera(knownWidth, focalLength, pixelWidth):
            return (knownWidth * focalLength) / pixelWidth
focal_length = 875

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    
    ret=True
    
    while (ret):
        
        ret, image_np=cap.read() 
    
        # Definite input and output Tensors for detection_graph
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        
          # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
          # Actual detection.
        (boxes, scores, classes, num) = sess.run(
              [detection_boxes, detection_scores, detection_classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
       
        vis_util.visualize_boxes_and_labels_on_image_array(
              image_np,
              np.squeeze(boxes),
              np.squeeze(classes).astype(np.int32),
              np.squeeze(scores),
              category_index,
              use_normalized_coordinates=True,
              line_thickness=8)

        objects = []
        class_str = ""
        height, width, channels = image_np.shape
        print("this is width: ", width)
        rows, cols = image_np.shape[:2]
        left_boundary = [int(cols*0.30), int(rows*0.95)]
        left_boundary_top = [int(cols*0.30), int(rows*0.20)]
        right_boundary = [int(cols*0.70), int(rows*0.95)]
        right_boundary_top = [int(cols*0.70), int(rows*0.20)]
        bottom_left  = [int(cols*0.05), int(rows*0.95)]
        top_left     = [int(cols*0.05), int(rows*0.20)]
        bottom_right = [int(cols*0.95), int(rows*0.95)]
        top_right    = [int(cols*0.95), int(rows*0.20)]
        vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
        cv2.line(image_np,tuple(bottom_left),tuple(bottom_right), (255, 0, 0), 5)
        cv2.line(image_np,tuple(bottom_right),tuple(top_right), (255, 0, 0), 5)
        cv2.line(image_np,tuple(top_left),tuple(bottom_left), (255, 0, 0), 5)
        cv2.line(image_np,tuple(top_left),tuple(top_right), (255, 0, 0), 5)
        copied = np.copy(image_np)
        interested=region_of_interest(copied,vertices)
        frame_expanded = np.expand_dims(interested, axis=0)

        ymin = int((boxes[0][0][0]*width))
        xmin = int((boxes[0][0][1]*height))
        ymax = int((boxes[0][0][2]*width))
        xmax = int((boxes[0][0][3]*height))
        Result = np.array(image_np[ymin:ymax,xmin:xmax])

        ymin_str='y min  = %.2f '%(ymin)
        ymax_str='y max  = %.2f '%(ymax)
        xmin_str='x min  = %.2f '%(xmin)
        xmax_str='x max  = %.2f '%(xmax)
        width = xmax - xmin
        width_str='width = %.2f '%(width)
        width_inc = xmax/75
        width_inc_str = 'width = %.2finches '%(width_inc)
        dist = distance_to_camera(width_inc, focal_length, width)
        dist_str = 'Distance = %.2finches '%(dist)
        
        cv2.putText(image_np,ymin_str, (50, 30),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
        cv2.putText(image_np,ymax_str, (50, 50),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
        cv2.putText(image_np,xmin_str, (50, 70),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
        cv2.putText(image_np,xmax_str, (50, 90),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
        cv2.putText(image_np,width_str, (50, 110),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
        cv2.putText(image_np,width_inc_str, (50, 130),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
        cv2.putText(image_np,dist_str, (400, 130),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)

        print(scores.max())
     
        print("left_boundary[0],right_boundary[0] :", left_boundary[0], right_boundary[0])
        print("left_boundary[1],right_boundary[1] :", left_boundary[1], right_boundary[1])
        print("xmin, xmax :", xmin, xmax)
        print("ymin, ymax :", ymin, ymax)
        if(xmin >= left_boundary[0]):
          cv2.putText(image_np,'Move LEFT!', (300, 100),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),2)
        elif(xmax <= right_boundary[0]):
          cv2.putText(image_np,'Move RIGHT!', (300, 100),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),2)
        elif(xmin <= left_boundary[0] and xmax >= right_boundary[0]):
          print("STOPPPPPP !!!! - 3nd !!!")
          cv2.putText(image_np,' STOPPPPPP!!!', (300, 100),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),2)
        cv2.line(image_np,tuple(left_boundary),tuple(left_boundary_top), (255, 0, 0), 5)
        cv2.line(image_np,tuple(right_boundary),tuple(right_boundary_top), (255, 0, 0), 5)
        #VideoFileOutput.write(image_np)
       
       
        print(coordinates)
        VideoFileOutput.write(image_np)
        cv2.imshow('live_detection',image_np)
        if cv2.waitKey(25) & 0xFF==ord('q'):
            break
            cv2.destroyAllWindows()
            cap.release()



