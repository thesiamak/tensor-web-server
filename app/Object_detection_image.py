import os
import cv2
import numpy as np
import tensorflow as tf
# Import utilites
from .utils import label_map_util
from .utils import visualization_utils as vis_util


class Detection:

    # Path to image
    PATH_TO_IMAGE = ""

    # Number of classes the object detector can identify
    NUM_CLASSES = 2

    def __init__(self, image_path, number_of_classes):
        print(image_path, number_of_classes)
        self.PATH_TO_IMAGE = image_path
        self.NUM_CLASSES = number_of_classes
        pass

    def detect(self):
        # Name of the directory containing the object detection module we're using

        # Grab path to current working directory
        BasePath = '/home/siamak/PycharmProjects/'
        # Path to frozen detection graph .pb file, which contains the model that is used
        # for object detection.
        PATH_TO_CKPT = BasePath + "tensor3/res/inference_graph/frozen_inference_graph.pb"

        # Path to label map file
        PATH_TO_LABELS = BasePath + "tensor3/res/training/labelmap.pbtxt"

        # Load the label map.
        # Label maps map indices to category names, so that when our convolution
        # network predicts `5`, we know that this corresponds to `king`.
        # Here we use internal utility functions, but anything that returns a
        # dictionary mapping integers to appropriate string labels would be fine
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

        # Load the Tensorflow model into memory.
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            sess = tf.Session(graph=detection_graph)

        # Define input and output tensors (i.e. data) for the object detection classifier

        # Input tensor is the image
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

        # Output tensors are the detection boxes, scores, and classes
        # Each box represents a part of the image where a particular object was detected
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represents level of confidence for each of the objects.
        # The score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

        # Number of objects detected
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        print('num_detections',num_detections)

        # Load image using OpenCV and
        # expand image dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        image = cv2.imread(self.PATH_TO_IMAGE)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_expanded = np.expand_dims(image_rgb, axis=0)
        results = []

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})

        # Draw the results of the detection (aka 'visulaize the results')
        for index in range(3):
            if scores[0][index] > 0.5 or len(results) < 3:
                results.append({'name': category_index[classes[0][index]]['name'], 'confidence': int(scores[0][index] * 100)})

        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)

        image_name = self.PATH_TO_IMAGE.split('/')[len(self.PATH_TO_IMAGE.split('/')) - 1]
        result_image_path = BasePath + "ODPyWS/" + self.PATH_TO_IMAGE[:self.PATH_TO_IMAGE.index(image_name)]
        image_name = result_image_path + "result_" + image_name
        cv2.imwrite(image_name, image)

        path_array = image_name.split('/')

        return {'output_image': '/trainer/download/%s/%s' % (path_array[len(path_array)-2], path_array[len(path_array)-1]),
                'objects': results, 'num_detections': len(results), 'total_detected': int(num[0])}
