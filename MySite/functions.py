import io
import os
import mammoth
from docx import Document
import docx


def handle_uploaded_file(f):
    file_stream = io.BytesIO(f.read())
    result = mammoth.convert_to_html(file_stream)
    text = result.value
    return text
    # fullText = []
    # document = Document(file_stream)
    # for para in document.paragraphs:
    #     fullText.append(para.text)
    # return fullText
