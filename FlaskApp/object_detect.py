import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import os
from collections import Counter


def object_detect(filename):
    """
    This function will detect objects in image
    """
    cv2.ocl.setUseOpenCL(False)
    just_fname = filename.split(".")[0]
    image = cv2.imread('./static/uploads/' + filename)
    bbox, label, conf = cv.detect_common_objects(image)
    output_image = draw_bbox(image, bbox, label, conf)
    plt.imshow(output_image)
    plt.savefig(os.path.join('./static/output/', just_fname + '.png'))
    d = Counter(label)
    if not label:
        return "No objects detected"
    labelstr = ", ".join('{} {}'.format(v, k) for k, v in d.items())
    return labelstr
