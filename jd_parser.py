import fitz
from docx import Document


def extract_pdf_text(file_path):

    text = ""

    document = fitz.open(file_path)

    for page in document:

        text += page.get_text()

    document.close()

    return text


def extract_docx_text(file_path):

    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:

        text.append(paragraph.text)

    return "\n".join(text)