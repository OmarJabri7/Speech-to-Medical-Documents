import cv2
import numpy as np
from sklearn.cluster import MeanShift

def find_line_regions(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Find horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
    horizontal = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    # # Find vertical lines
    # vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,25))
    # vertical = cv2.morphologyEx(edges, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

    # Combine the horizontal and vertical lines
    # lines = cv2.addWeighted(horizontal, 0.5, vertical, 0.5, 0.0)

    # Find contours of the lines
    contours, hierarchy = cv2.findContours(horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the bounding boxes of the line regions
    line_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # if w > img.shape[1] * 0.9: # Ignore regions that are the full width of the image
        #     continue
        # if h < img.shape[0] * 0.02: # Ignore regions that are less than 2% of the height of the image
        #     continue
        line_regions.append((x, y, w, h))
    # Use MeanShift clustering to group the line regions
    X = np.array(line_regions)
    bandwidth = X.shape[0] // 10 # Adjust this value to control the clustering sensitivity
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_

    # Group the line regions by cluster label
    line_blocks = {}
    for label in np.unique(labels):
        line_blocks[label] = [line_regions[i] for i in np.where(labels == label)[0]]

    return line_blocks

if __name__ == "__main__":
    img = cv2.imread('../data/form5.jpeg')
    line_blocks = find_line_regions(img)

    # Draw rectangles around the line blocks
    for i, (label, line_regions) in enumerate(line_blocks.items()):
        for (x, y, w, h) in line_regions:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
