import numpy as np
import skimage.io as io
from loguru import logger
import os
import numpy as np
import csv
from PIL import Image
from tqdm import tqdm
from os.path import join as pathj
import glob
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from statistics import median


def save_w_or_h(arry, csvname, parms=None):
    arry = np.array(arry)
    # parms = [25,50,75,90,95,98,99,99.5]
    if not parms:
        parms = np.linspace(25, 100 ,4)
    percent_nums ={}
    save_to_csv(arry, csvname, parms, percent_nums)
    import json
    print(json.dumps(percent_nums,indent=2))

def save_to_csv(arry, csvname, parms, percent_nums):
    csv_file = open(csvname, 'w', newline='', encoding='utf-8')
    # 调用open()函数打开csv文件，传入参数：文件名“demo.csv”、写入模式“w”、newline=''、encoding='gbk'
    writer = csv.writer(csv_file)
    for parm in parms:
        try:
            percent_nums[str(parm)+'%'] = np.percentile(arry, parm)
            writer.writerow([str(parm)+'%', np.percentile(arry, parm)])

        except:
            pass
    csv_file.close() 

def save_wh_dist_csv(domain_key, domain_num, csvname):
    with open(csvname, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(20):
            ratio = round(domain_num[i]/5644, 2)
            print(f'{domain_key[i]} {domain_num[i]} {ratio}')
            writer.writerow([domain_key[i], domain_num[i], ratio])
            

IMAGE_FORMAT = ['png','jpg']
if __name__ == '__main__':
# from01 = glob.glob(f'{root}/{test_folder}/annotations/*')
    imgr_dir = r'E:\visDrone2019\VisDrone2019-DET-train' 
    imgs_dir = pathj(imgr_dir, 'images')

    img_name_l = [x for x in os.listdir(imgs_dir) if x in IMAGE_FORMAT]
    list_l = []
    per_x =[]
    per_y =[]
    for img_name in tqdm(img_name_l):
        img = Image.open(pathj(imgs_dir, img_name))
        w = img.width       #图片的宽
        h = img.height
        key = str(w)+'@'+ str(h)
        list_l.append(key)
        per_x.append(w)
        per_y.append(h)
    unique_classes, nt = np.unique(list_l, return_counts=True)
    i = nt.argsort()[::-1]
    domain_key = unique_classes[i]
    domain_num = nt[i]
    # parms = [1, 5,15,25,30,35,40,45,50,75,95]
    # save_w_or_h(per_x,'width.csv', parms)
    # save_w_or_h(per_y,'height.csv', parms)
    save_wh_dist_csv(domain_key,domain_num,'imgsz_dist.csv')
    print('hello')