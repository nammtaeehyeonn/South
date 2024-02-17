from PIL import Image
import PyPDF2

image1 = Image.open('/mnt/e/South/entry_example.jpg')
im1 = image1.convert('RGB')
im1.save('/mnt/e/South/entry_example.pdf')

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    print(text)
    return text

extract_text_from_pdf(im1)

