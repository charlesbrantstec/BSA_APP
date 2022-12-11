from docx import Document
from docx.shared import Inches
from docx.shared import Pt

document = Document()

style = document.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)

paragraph_format = style.paragraph_format
# paragraph_format.line_spacing = Pt(24)

p = document.add_paragraph()
# p.alignment = WD_ALIGN_PARAGRAPH.CENTER
l1 = p.add_run('1.Name:____________________________________________________________   \n    \
                  Address:_________________________________________________________')
# l2 = p.add_run('  Address:_________________________________________________________')	
# l2 = p.add_run('  EIN/ITIN/SS#:_____________________________')	
# l3 = p.add_run('  1099 Amount Paid: $______________ W2 Amount Paid: $______________')			





document.save('test.docx') 