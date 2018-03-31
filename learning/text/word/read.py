import docx
doc = docx.Document('/home/kcp/test/q.docx')
for para in doc.paragraphs :
    print(para.text)