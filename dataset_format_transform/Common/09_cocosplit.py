# -*- coding: utf-8 -*-
from __future__ import print_function
"""
Created on 2021/12/9

@author: Totie
"""

'''
从coco的标注文件里提取一张图片对应的json信息，并保存成新的json文件（以instance为例，其他的类似）。
'''
import matplotlib.pyplot as plt
import os, sys, zipfile
import urllib.request
import shutil
import numpy as np
# import skimage.io as io
import pylab
import json
from pycocotools.coco import COCO

pylab.rcParams['figure.figsize'] = (8.0, 10.0)
dataset_path = './coco'
image_path = 'val2017'
json_file='/root/CenterNet-ht/Center/data/coco/annotations/train.json' # # json源文件

coco=COCO(json_file)
data=json.load(open(json_file,'r')) 

data_2={}   #新json文件

data_2['info']=data['info']
data_2['licenses']=data['licenses']
data_2['categories']=data['categories']

annotation=[]
images = []
# print(data_img['images'])

imagename = [f for f in os.listdir(os.path.join(dataset_path, image_path))] #读取文件夹下图片名字
print(len(data['images'])) 

#根据图片数量找到每张图片对应的annotation，即每个‘images’可能有多个annotation（一张图片有多个可识别的目标）
for name_index in range(0,len(imagename)):
    # 通过imgID 找到其所有instance
    imgID = 0
    for i in range(0,len(data['images'])):
        if data['images'][i]['file_name'] == imagename[name_index]:  #根据图片名找到对应的json中的'images'
            imgID = imgID=data['images'][i]['id']
            print(name_index, imgID)  

    for ann in data['annotations']:    #根据image_id找到对应的annotation
        if ann['image_id']==imgID:
            annotation.append(ann)

data_2['annotations']=annotation
data_2['images'] = images
print(len(data_2['annotations']))
# 保存到新的json

json.dump(data_2,open('./val2017.json','w'),indent=4)
# 从coco标注json中提取单张图片的标注信息
