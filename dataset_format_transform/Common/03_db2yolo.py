# -*- coding: UTF-8 -*-
import json
import os
from os.path import join as pathj
# from loguru import logger
from PIL import Image

def xyxy2cxcy(img_size, box):
    x1,y1,x2,y2 = int(box[0]),int(box[1]),int(box[2]),int(box[3])
    if x1 < 0:
        x1 = 0.0
        print("\033[0;33;33m", "越界检查,x1小于0,错误数据:", x1, "已修订为:", "\033[0m")

    elif x1 > img_size[0]:
        x1 = float(img_size[0])
        print("\033[0;33;33m", "越界检查,x1大于宽,错误数据:", x1, "已修订为:", "\033[0m")

    if y1 < 0:
        y1 = 0.0
        print("\033[0;33;33m", "越界检查,y1小于0,错误数据:", y1, "已修订为:","\033[0m")

    elif y1 > img_size[1]:
        y1 = float(img_size[1])
        print("\033[0;33;33m", "越界检查,y1大于高,错误数据:", y1, "已修订为:","\033[0m")

    if x2 < 0:
        x2 = 0.0
        print("\033[0;33;33m", "越界检查,x2小于0,错误数据:", x2, "已修订为:", "\033[0m")

    elif x2 > img_size[0]:
        x2 = float(img_size[0])
        print("\033[0;33;33m", "越界检查,x2大于宽,错误数据:", x2, "已修订为:",  "\033[0m")

    if y2 < 0:
        y2 = 0.0
        print("\033[0;33;33m", "越界检查,y2小于0,错误数据:", y2, "已修订为:","\033[0m")

    elif y2 > img_size[1]:
        y2 = float(img_size[1])
        print("\033[0;33;33m", "越界检查,y2大于高,错误数据:", y2, "已修订为:", "\033[0m")
    # 2.转换并归一化
    center_x = (x1 + x2) * 0.5 / img_size[0]
    center_y = (y1 + y2) * 0.5 / img_size[1]
    w = abs((x2 - x1)) * 1.0 / img_size[0]
    h = abs((y2 - y1)) * 1.0 / img_size[1]
    return center_x, center_y, w, h

#C:\Users\tingfeng-wu\Desktop\github\mywork\0003_cv-workspace\common\py_util\util.py
def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def line2str(l):
    str1=''
    for ele in l[0:-1]:
        str1 = str1 + str(ele)+' '
    return str1 + str(l[-1])


#--- folder path：data目录
root_dir = '/workspace/bohuang/data/dbnet/f27_order'

save_dir = '/data/screen_analysis/0002_sa_task/0007_tingfeng_yolo'#保存路径 images,labels

train_link = 'train'
test_link = 'test'

train_label_path = pathj(root_dir, 'train', 'label') #原始标注位置
train_img_path = pathj(root_dir, 'image') # iamge

train_coco_label_path = pathj(save_dir, 'cocolabels', 'train')
ensure_dir(train_coco_label_path)
#-----
#---
classes = ['icon','text','image']
cls2id = {}
for k,v in enumerate(classes):
    cls2id[v] = k
#---

file_list = os.listdir(train_label_path)
logger.info("total: %s" % (len(file_list)))
count = 0
for file in file_list:
    file_path = pathj(train_label_path, file)
    #label 名字
    save_name = file[3:-4]+'.txt'
    
    img = Image.open(pathj(train_img_path ,file[3:-4])+'.png')#txt怎么取名的这个问题
    txt = []
    with open(file_path,'r',encoding='utf-8') as f:
        for line in f.readlines():
            row = line.strip().split(',')
            x1 = row[0]
            y1 = row[1]
            x2 = row[4]
            y2 = row[5]
            cls = row[-1]
            cx,cy,w,h = xyxy2cxcy(img.size,[x1,y1,x2,y2])
            new_line = [cls2id[cls],cx,cy,w,h]
            txt.append(new_line)
        # print(txt)
        abs_save_name = pathj(train_coco_label_path,save_name)
        #logger.info(abs_save_name)
        with open(abs_save_name, "w") as f:
            for row in txt:
                line = line2str(row)
                f.write(line +'\n')  # 自带文件关闭功能，不需要再写f.close()
            count+=1
print('total transform: %s'% (count))