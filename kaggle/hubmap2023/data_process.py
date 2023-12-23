import os

imgpath = r'D:\data\hubmap_imagenet\train'
image_all = [x for x in os.listdir(imgpath)]

#提取有标注的图片
import json

imgid_anno = []
with open(r'D:\data\hubmap_imagenet\polygons.jsonl', 'r') as f:
    for line in f:
        imgid_anno.append(json.loads(line)['id']+'.tif')

# 计算差集
img_unlabeled = list(set(image_all).difference(set(imgid_anno)))

print(len(image_all))
print(len(imgid_anno))

import os
import random
import shutil
train_percent = 0.8
val_percent = 0.2
train_size = int(len(img_unlabeled) * train_percent)
val_size = len(img_unlabeled) - train_size
random.shuffle(img_unlabeled)

train_set = img_unlabeled[:train_size]
val_set = img_unlabeled[train_size:]
from os.path import join as pathj
# new_train_path = pathj
if not os.path.exists('./train_set'):
    os.mkdir('./train_set')
if not os.path.exists('./val_set'):
    os.mkdir('./val_set')


for item in train_set:
    filePath = os.path.join(imgpath, item)
    savePath = os.path.join('train_set', item)
    shutil.copyfile(filePath, os.path.join(savePath)) #

for item in val_set:
    filePath = os.path.join(imgpath, item)
    savePath = os.path.join('val_set', item)
    shutil.copyfile(filePath, os.path.join(savePath)) #