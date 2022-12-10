from docx import Document
from docx.shared import Inches
from docx.shared import Pt

document = Document()

run = document.add_paragraph('Hi').add_run()
font = run.font
font.name = 'Calibri'   
font.size = Pt(26)

document.save('test.docx')