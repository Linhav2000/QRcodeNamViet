import numpy as np
import tensorflow as tf
import cv2

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from CommonAssit.FileManager import *
from tkinter import messagebox
import sys
import six

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile

detection_model = None
category_index = None

def load_model(model_path):
    model = tf.saved_model.load(model_path)
    return model


def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # Run inference
    output_dict = model(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key: value[0, :num_detections].numpy()
                   for key, value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            output_dict['detection_masks'], output_dict['detection_boxes'],
            image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()

    return output_dict

def processImage(image, matching_value=0.5, resize_shape=(-1, -1)):
    global detection_model
    resizeImage = image.copy()
    if resize_shape != (-1, -1):
        width = resize_shape[0] if resize_shape[0] > 0 else resizeImage.shape[1]
        height = resize_shape[1] if resize_shape[1] > 0 else resizeImage.shape[0]
        resizeImage = cv2.resize(image, dsize=(width, height))

    output_dict = run_inference_for_single_image(detection_model, resizeImage)
    valid_boxes, class_names = get_valid_boxes(boxes=output_dict['detection_boxes'],
                                                scores=output_dict['detection_scores'],
                                                classes=output_dict['detection_classes'],
                                                image=image,
                                                min_score_thresh=matching_value)
    # print(f"time process: {time.time() - _time}")
    return valid_boxes, class_names

def get_valid_boxes(boxes, scores,classes, image, min_score_thresh=0.5):
    global category_index
    im_width = image.shape[1]
    im_height = image.shape[0]
    valid_boxes = []
    class_names = []
    for i in range(boxes.shape[0]):
        if scores is None or scores[i] > min_score_thresh:
            if classes[i] in six.viewkeys(category_index):
              class_name = category_index[classes[i]]['name']
            else:
              class_name = 'N/A'
            display_str = str(class_name)
            ymin, xmin, ymax, xmax = tuple(boxes[i].tolist())

            valid_box = (int(xmin * im_width), int(ymin * im_height),
                                                int(xmax * im_width), int(ymax * im_height))

            valid_boxes.append(valid_box)
            class_names.append(display_str)

    return valid_boxes, class_names

def init_model():
    global detection_model
    global category_index
    algorithmPath = ""
    try:
        algorithm_file = TextFile("config/algorithm_path.txt")
        algorithmPath = algorithm_file.readFile()[0].replace("\n", "")
    except:
        messagebox.showerror("Algorithm read failed", "Please check the algorithm file path!")
        sys.exit()
    model_save_path = rf"{algorithmPath}/saved_model"
    map_path = rf"{algorithmPath}/map.pbtxt"
    detection_model = load_model(model_save_path)
    category_index = label_map_util.create_category_index_from_labelmap(map_path, use_display_name=True)
