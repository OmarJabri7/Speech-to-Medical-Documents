import os

import cv2
import pytesseract as pt
from utils import image_functions as img
import pandas as pd
import numpy as np

def analyze_doc(folders):
    print(os.getcwd())
    print(os.listdir())
    form = cv2.imread(f'{folders[0]}/form.jpeg')
    form_gray = img.get_grayscale(form)

    blur = cv2.GaussianBlur(form_gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    all_texts = pd.DataFrame([], columns=["Sections"])
    pdf = pt.image_to_pdf_or_hocr(f'{folders[0]}/form.jpeg', extension='pdf')
    with open(f'{folders[1]}/form.pdf', 'w+b') as f:
        f.write(pdf)  # pdf type is bytes by defaultxww
    counter = 0
    print(len(cnts))
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        sub_img = form[x:x + h, x:x + w]
        text = pt.image_to_string(sub_img)
        text_dat = pd.DataFrame(text.split("\n\n"))
        all_texts = all_texts.append(pd.DataFrame(np.array(text_dat, dtype=str)))
        img_dat = pt.image_to_data(sub_img)
        rect = cv2.rectangle(form, (x, y), (x + w, y + h), (36, 255, 12), 2)
        # if counter == 2:
        #     fontFace = cv2.FONT_HERSHEY_PLAIN
        #     fontScale = 0.5
        #     color = (0, 0, 0)
        #     # lineType = cv2.LINE_4
        #     cv2.putText(rect, "HEY BITCH", (x, y - 50), fontFace, fontScale, color)
        counter+=1
    all_texts.to_csv(f'{folders[1]}/form.csv', index=False)
    cv2.imwrite(f'{folders[1]}/form.png', form)

if __name__ == "__main__":
    pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    analyze_doc(["data","output"])
