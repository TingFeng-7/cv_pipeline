# -*- coding: UTF-8 -*-
import json
import os
from os.path import join as pathj
# from loguru import logger
from PIL import Image

# 1. labelme的框框可能会越界
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
    # 2.转换并归一化 robust
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

def gen_class2id(classes):
    cls2id = {}
    for k,v in enumerate(classes):
        cls2id[v] = k
    return cls2id

if __name__ == '__main__':
#--- folder path：data目录
    label_dir = r'C:\Users\tingfeng-wu\Desktop\02_github\py_script\data_format_transform\01 NWPU VHR-10 dataset\gt'
    imgs_dir = r'C:\Users\tingfeng-wu\Desktop\02_github\py_script\data_format_transform\01 NWPU VHR-10 dataset\gtwithimg'
    save_dir = r'yolo gt2'#保存路径 images,labels
    ensure_dir(save_dir)
    count = 0 

    for name in [x for x in os.listdir(label_dir) if x.endswith('txt')]:
        print(name)
        label_name = os.path.join(label_dir,name)
        save_name = os.path.join(save_dir,name)
        img_name = pathj(imgs_dir, name[:-4]+'.jpg')
        txt =[]
        count = 0
        img = Image.open(img_name)#txt怎么取名的这个问题
        with open(label_name,'r',encoding='utf-8') as f:
            for line in f.readlines():
                row = line.strip().replace('(',"").replace(')',"").split(',')
                if len(row) < 4 : continue
                x1 = row[0]
                y1 = row[1]
                x2 = row[2]
                y2 = row[3]
                cls = row[-1] 
                cx,cy,w,h = xyxy2cxcy(img.size,[x1,y1,x2,y2])
                new_line = [int(cls)-1,cx,cy,w,h]
                txt.append(new_line)

            with open(save_name, "w") as f:
                for row in txt:
                    line = line2str(row)
                    f.write(line +'\n')  # 自带文件关闭功能，不需要再写f.close()
                count+=1
    print('total transform: %s'% (count))