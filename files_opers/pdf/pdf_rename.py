import os

def rename_pdf(pdf_dir):
    pdf_list = os.listdir(pdf_dir)
    for pdf in pdf_list:
        if pdf.startswith('扫描_') and pdf.endswith('.pdf'):
            pdf_num = pdf.split(' ')[-1].replace('(', '').replace(')', '')
            pdf_num = int(pdf_num)
            
            if len(str(pdf_num)) == 1:
                new_pdf_name = '扫描_20230526_0'+str(pdf_num)+'.pdf'
            else:
                new_pdf_name = '扫描_20230526_'+str(pdf_num)+'.pdf'    
            
            os.rename(os.path.join(pdf_dir, pdf), os.path.join(pdf_dir, new_pdf_name))

if __name__ == '__main__':
    dir = r'C:\Users\tinfengwu\Pictures\scan'
    rename_pdf(dir)