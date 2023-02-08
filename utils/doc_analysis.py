import os

import cv2
import pytesseract as pt
# import image_functions as img
import pandas as pd
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
    x, y, width, height = dims_uint
    x += 2
    width -= 20

    text_height = height - 20
    text_area = Image.new('RGB', (width, text_height), (255, 255, 255))
    draw = ImageDraw.Draw(text_area)

    font = ImageFont.truetype("arial.ttf", 12)
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

    padding = 10
    y_pos = padding
    for line in text_lines_wrap:
        draw.text((0, y_pos), line, (0, 0, 0), font=font)
        y_pos += draw.textsize(line, font)[1]

    text_area = text_area.convert("RGBA")
    img.paste(text_area, (x, y + 15), text_area)
    return img



def analyze_doc(folders, form):
    rois, dims = extract_text_areas(f'{folders[0]}/{form}.jpeg')

    all_texts = pd.DataFrame([], columns=["Sections"])
    cnt = 0
    for roi in rois:
        text = pt.image_to_string(roi)
        text_dat = pd.DataFrame(text.split("\n\n"))
        all_texts = all_texts.append(pd.DataFrame(np.array(text_dat, dtype=str)))
        # img_dat = pt.image_to_data(roi)
        # cv2.imwrite(f'{folders[1]}/sub_imgs/{text}.jpeg', roi)
        im_pil = Image.fromarray(roi)
        text = text.replace("\n", "").replace("'", "")
        text = re.sub("\W+",' ', text )
        im_pil.save(rf'{folders[1]}/sub_imgs/{text} {" ".join(str(x) for x in dims[cnt])} .jpeg')
        cnt+=1
    all_texts.to_csv(rf'{folders[1]}/form.csv', index=False)
    # cv2.imwrite(f'{folders[1]}/form.png', form)

if __name__ == "__main__":
    pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    analyze_doc(["../data","../output"], "gp")
