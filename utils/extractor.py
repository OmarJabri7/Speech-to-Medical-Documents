import cv2
import numpy as np


def extract_text_areas(img_dir):
    # Load the image
    img = cv2.imread(img_dir)

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
        if cv2.contourArea(cnt) < 500:
            continue

        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(cnt)

        # Extract the rectangle text area from the image
        rois.append(img[y:y + h, x:x + w])
        dims.append([x,y,w,h])
        # Display the extracted text area
        cv2.imshow('ROI', img[y:y + h, x:x + w])
        cv2.waitKey(0)
    return rois, dims
