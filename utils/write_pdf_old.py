from extractor import extract_text_areas
import img2pdf
import pdfrw
import cv2

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
                Ff=0,
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
    pdf_file.write(img2pdf.convert(image_file))
rois, dims = extract_text_areas(cv2.imread(input_image_path))
template_pdf = pdfrw.PdfReader(output_pdf_path)
fields = []
cnt = 0
for dim in dims:
    x, y, w, h = dim
    # constrain fillable box within the rectangle
    # if w > h:
    #     w = h
    # else:
    #     h = w
    # field_rect = [
    #     dim[0],
    #     int(template_pdf.pages[0].MediaBox[3])-y-h,
    #     dim[0]+w,
    #     int(template_pdf.pages[0].MediaBox[3])-y
    # ]
    dim[2]/=2
    dim[3]/=2
    field_rect = [dim[0], int(template_pdf.pages[0].MediaBox[3]) - dim[1] - dim[3], dim[0] + dim[2],
                  int(template_pdf.pages[0].MediaBox[3]) - dim[1] - dim[3] + dim[3]]
    fields.append({'name': f"Field{cnt}", 'rect': field_rect})
    cnt += 1

# Add form fields to PDF
add_form_fields(template_pdf, fields)
pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
