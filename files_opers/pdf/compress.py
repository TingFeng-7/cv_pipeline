import fitz

pdf = fitz.open('original.pdf')

for page in pdf:
    page.compress_page()

pdf.save('compressed.pdf')  # 新建文件    