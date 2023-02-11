import os

import cv2
import pytesseract as pt
# import image_functions as img
import pandas as pd
from math import ceil
import numpy as np
from utils.extractor import extract_text_areas
from PIL import Image
import re

def take_notes(block, text, form, img=None):
    from PIL import Image, ImageDraw, ImageFont
    if img is None:
        img = Image.open(f"data/{form}.jpeg")
    block = block.split(" ")
    block.remove(".jpeg")
    dims = block[-4:len(block)]
    dims_uint = [int(dim) for dim in dims]
    font_size = float(block[-5])
    x, y, width, height = dims_uint
    x += 2
    y += int(font_size*4)
    text_height = height
    text_area = Image.new('RGBA', (width, text_height), (255, 255, 255))
    datas = text_area.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    text_area.putdata(newData)
    draw = ImageDraw.Draw(text_area)

    font = ImageFont.truetype("arial.ttf", ceil(12+(12%font_size)))
    text_lines = text.split(" ")

    text_lines_wrap = []
    line = ""
    for word in text_lines:
        if draw.textsize(line + word, font)[0] <= width:
            line = line + word + " "
        else:
            text_lines_wrap.append(line)
            line = word + " "
    text_lines_wrap.append(line)

    padding = 0
    y_pos = padding
    for line in text_lines_wrap:
        draw.text((0, y_pos), line, (0, 0, 0), font=font)
        y_pos += draw.textsize(line, font)[1]

    # text_area = text_area.convert("RGBA")
    img.paste(text_area, (x, y), text_area)
    return img

def check_font_size(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Otsu thresholding
    thresh, thresh_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find the contours of the text
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over each contour
    for contour in contours:
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Compute the aspect ratio of the bounding box
        aspect_ratio = float(w) / h

        # Check if the aspect ratio is within a certain range (to filter out non-text contours)
        if aspect_ratio > 0.1 and aspect_ratio < 10:
            # Compute the font size as the average height of the bounding box
            font_size = int(np.mean([h, w]))
            return font_size/100


def analyze_doc(folders, form):
    rois, dims = extract_text_areas(f'{folders[0]}/{form}.jpeg')

    all_texts = pd.DataFrame([], columns=["Sections"])
    cnt = 0
    for roi in rois:
        text = pt.image_to_string(roi)
        font_size = check_font_size(roi)
        text_dat = pd.DataFrame(text.split("\n\n"))
        all_texts = all_texts.append(pd.DataFrame(np.array(text_dat, dtype=str)))
        im_pil = Image.fromarray(roi)
        text = text.replace("\n", "").replace("'", "")
        text = re.sub("\W+",' ', text )
        if font_size:
            if font_size >= 1:
                im_pil.save(rf'{folders[1]}/sub_imgs/{text} {font_size} {" ".join(str(x) for x in dims[cnt])} .jpeg')
        cnt+=1
    all_texts.to_csv(rf'{folders[1]}/form.csv', index=False)
    # cv2.imwrite(f'{folders[1]}/form.png', form)

if __name__ == "__main__":
    pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    analyze_doc(["../data","../output"], "form")
