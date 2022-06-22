from reportlab.pdfbase import pdfform
from reportlab.lib.colors import magenta, pink, blue, green
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os
from reportlab.lib.pagesizes import letter


def do_pdf(text):
    c = canvas.Canvas('simple_form.pdf')

    c.setFont("Courier", 20)

    c.drawString(10, 450, 'Omar')

    c.save()

    packet = io.BytesIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica', 4)
    can.drawString(11, 123, text)
    # can.create_text(100, 100, text="LAABLE FEE")
    can.showPage()
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    print(os.getcwd())
    print(os.listdir())
    # Read your existing PDF
    existing_pdf = PdfFileReader(open("output/form.pdf", "rb"))
    output = PdfFileWriter()
    # Add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # Finally, write "output" to a real file
    outputStream = open("destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

#
# if __name__ == '__main__':
