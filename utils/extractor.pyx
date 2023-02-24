# distutils: language=c++
# cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True

cimport cython
from collections import defaultdict

import cv2
cimport numpy as np
import numpy as np
import pytesseract as pt
import enchant
import re
from libc.stdio cimport printf

from Cython import bint

def is_english_word(word):
    dictionary = enchant.Dict("en_US")
    return dictionary.check(word)

cdef bint is_number(str word):
    try:
        float(word)
        return True
    except ValueError:
        return False

def extract_text_areas(img):
    # Load the image

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to the grayscale image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Loop through all contours
    rois, dims = [], []
    for cnt in cnts:
        # Check if the contour is sufficiently large
        cnt = np.array(cnt, dtype=np.float32)
        if cv2.contourArea(cnt) < 250:
            continue

        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(cnt)
        roi = img[y:y + h, x:x + w]
        # Extract the rectangle text area from the image
        if roi.shape[0] < img.shape[0]/2 or roi.shape[1] < img.shape[1]/2:
            rois.append(roi)
            dims.append([x,y,w,h])
        # Display the extracted text area
    return rois, dims

from cython cimport boundscheck, wraparound


def distance_to_dim(coord, dim):
    return abs(coord - dim[1])

# Define the lambda function outside of the get_closest_text_box function
def distance_to_dim_lambda(dim):
    return lambda y: distance_to_dim(y, dim)

def get_closest_text_box(dim, coords, stop_words, text_orig):
    while True:
        y_coords = list(coords.keys())
        y_coords_ = [y for y in y_coords if y < dim[1]]
        if y_coords_:
            coord = min(y_coords_, key=lambda y: abs(y - dim[1]))
            text = coords[coord]
            # text = re.sub("\W+", ' ', text).strip()
            text = re.sub(r'[^a-zA-Z ]', '', text)
            text = text.lower().replace('yes', '').replace('no', '')
            text = text.lstrip().rstrip()
            text_list = [word for word in text.split(" ") if word.strip()]
            text = ' '.join(list(set(text_list)))
            if not text.isspace() and text not in stop_words and len(text) > 0:
                checker_text = re.sub(r'\s+', ' ', text)
                eng_words = [is_english_word(word) and not is_number(word) for word in checker_text.strip().split(' ') if not word.isspace()]
                if sum(1 for b in eng_words if b) >= int(len(text.strip().split(' '))/2): return text
                else: del coords[coord]
            else:
                del coords[coord]
        else:
            return ""
    return ""

cpdef extract_text_coords(np.ndarray[np.uint8_t, ndim=3] img):
    cdef np.ndarray[np.uint8_t, ndim=2] gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cdef np.ndarray[np.uint8_t, ndim=2] thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10)
    cdef np.ndarray[np.uint8_t, ndim=2] horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    cdef np.ndarray[np.uint8_t, ndim=2] morphology = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=3)
    contours, _ = cv2.findContours(morphology, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    data = pt.image_to_data(img, output_type='dict')
    boxes = len(data['level'])
    coords = dict()
    cdef str block
    for i in range(boxes):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        # Extract block of text
        block = ""
        for j in range(len(data['text'])):
            if (data['left'][j] >= x and data['left'][j] + data['width'][j] <= x + w and
                    data['top'][j] >= y and data['top'][j] + data['height'][j] <= y + h):
                block += data['text'][j] + " "
        # Add block to dictionary
        if y + h in coords:
            coords[y + h]+= block + " "
        else:
            coords[y + h] = block + " "
    return coords