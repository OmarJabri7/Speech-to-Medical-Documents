from pdf2image import convert_from_path

# Convert the PDF to a list of images
images = convert_from_path('data/gp.pdf')

# Combine all images into a single image
images[0].save('data/gp.png', "PNG", save_all=True, append_images=images[1:])
