# Installation Instructions
## TensorFlow Installation
TensorFlow was installed using the instruction's on TensorFlow's github [installation page](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)

## Running the Code
Using Anaconda to run this code, makes your life much easier because all of the modules in the code are already imported.  After TensorFlow has installed, run `ROI_tensorflow.py` as a python script or on jupyter notebook.

The model currently loaded in the code is the Open Images pretrained model on [TensorFlow's github](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)
If you want to use a different model, modify the code:
```
MODEL_NAME = 'faster_rcnn_inception_resnet_v2_atrous_oid_v4_2018_12_12'
.
.
PATH_TO_LABELS = os.path.join('data', 'oid_v4_label_map.pbtxt')
```
to the model that you want with its corresponding [label map](https://github.com/tensorflow/models/tree/master/research/object_detection/data)
