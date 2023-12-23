# Python使用PyPDF2

from PyPDF2 import PdfMerger
import os
import os.path as osp

import fitz


pdf_dir = r'C:\Users\tinfengwu\Pictures\scan'

pdf_list0 = os.listdir(pdf_dir)[:10]
pdf_list1 = os.listdir(pdf_dir)[10:]

def merge_pdf(pdf_dir, pdf_list, name):
    merger = PdfMerger()
    print(pdf_list)
    for pdf in pdf_list:
        merger.append(osp.join(pdf_dir, pdf))

    desktop = r'C:\Users\tinfengwu\Desktop'
    merger.write(osp.join(desktop, 'result'+str(name)+'.pdf'))
    print(osp.join(desktop, 'result'+str(name)+'.pdf'))

merge_pdf(pdf_dir, pdf_list0, 0)
merge_pdf(pdf_dir, pdf_list1, 1)

# pdf = fitz.open(osp.join(desktop, 'result.pdf'))
# for page in pdf:
#     # page.compress_page()
#     page.setCompression('Flate') 

# pdf.save(osp.join(desktop, 'result_compress.pdf'))  # 新建文件    