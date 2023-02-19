import cv2
import img2pdf
import pdfrw
from extractor import extract_text_areas

def add_form_fields(template_pdf, fields):
    """
    Add form fields to a PDF file using pdfrw.
    :param template_pdf: a pdfrw.PdfReader instance representing the input PDF file.
    :param fields: a list of dictionaries representing the form fields to add to the PDF file.
        Each dictionary should have the following keys:
            - name: the name of the form field.
            - rect: a list of four numbers representing the position and size of the form field in points.
    """
    template_pdf.Root.AcroForm = pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'))
    for page in template_pdf.pages:
        annotations = page.Annots or []
        for field_data in fields:
            new_field = pdfrw.PdfDict(
                FT=pdfrw.PdfName('Tx'),
                Subtype=pdfrw.PdfName('Widget'),
                Rect=pdfrw.PdfArray(field_data['rect']),
                DA='/Helv 8 Tf 0 g',
                T=field_data['name'],
                V='',
                Ff=4096,  # Add multi-line option
                Type=pdfrw.PdfName('Annot'),
                Border=pdfrw.PdfArray([0, 0, 0]),
                H=pdfrw.PdfName('N')
            )
            annotations.append(new_field)
        page.Annots = annotations

input_image_path = '../data/gp1024_2.jpeg'
output_pdf_path = 'output.pdf'

# Convert JPEG to PDF
with open(input_image_path, 'rb') as image_file, open(output_pdf_path, 'wb') as pdf_file:
    try:
        pdf_file.write(img2pdf.convert(image_file))
    except Exception as e:
        print(f'Error converting image to PDF: {e}')
        exit(1)

# Extract text areas from the image
rois, dims = extract_text_areas(cv2.imread(input_image_path))

# Create form fields from the text areas
template_pdf = pdfrw.PdfReader(output_pdf_path)
fields = []
field_count = 0
for dim in dims:
    x, y, w, h = dim
    field_rect = [
        x,
        int(template_pdf.pages[0].MediaBox[3]) - y - h,
        x + w,
        int(template_pdf.pages[0].MediaBox[3]) - y
    ]
    fields.append({'name': f"Field{field_count}", 'rect': field_rect})
    field_count += 1

# Add form fields to PDF
add_form_fields(template_pdf, fields)

# Save the updated PDF
with open(output_pdf_path, 'wb') as pdf_file:
    try:
        pdfrw.PdfWriter().write(pdf_file, template_pdf)
    except Exception as e:
        print("Error writing pdf")