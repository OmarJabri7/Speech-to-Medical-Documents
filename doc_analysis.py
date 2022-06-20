import cv2
import pytesseract as pt
import utils.image_functions as img
import pandas as pd
import numpy as np
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,portrait

if __name__ == "__main__":
    form = cv2.imread('data/form.jpeg')
    form_gray = img.get_grayscale(form)

    blur = cv2.GaussianBlur(form_gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    all_texts = pd.DataFrame([], columns=["Sections"])
    pdf = pt.image_to_pdf_or_hocr('data/form.jpeg', extension='pdf')
    with open('output/form.pdf', 'w+b') as f:
        f.write(pdf)  # pdf type is bytes by defaultxww
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        sub_img = form[x:x + h, x:x + w]
        text = pt.image_to_string(sub_img)
        text_dat = pd.DataFrame(text.split("\n\n"))
        all_texts = all_texts.append(pd.DataFrame(np.array(text_dat, dtype=str)))
        img_dat = pt.image_to_data(sub_img)
        cv2.rectangle(form, (x, y), (x + w, y + h), (36, 255, 12), 2)
    all_texts.to_csv('output/form.csv', index=False)
    cv2.imwrite('output/form.png', form)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(10, 100, "Hello world")
    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("output/form.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
