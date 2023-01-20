import sys
sys.path.append(r'C:\Users\tingfeng-wu\Desktop\02_github\py_script')
sys.path.append(r'C:\Users\tingfeng-wu\Desktop\02_github\py_script\cocoapi\PythonAPI')
from pycocotools.coco import COCO
from utils.utils1 import *
import os.path as osp


# 总的json 一个split
ori_coco_json_path = r'D:\sa_data\0010_v1.5_filtered_linebox_yolox\coco\train_oneclass_12.json'
ori_coco_ins = read_json_instance(ori_coco_json_path)
coco=COCO(ori_coco_json_path)

data_2={}   #新json文件
data_2['info']=ori_coco_ins['info']
# data_2['licenses']=ori_coco_ins['licenses']
data_2['categories']=ori_coco_ins['categories']
data_2['annotations']=[]
data_2['images']=[]

data_3={}   #新json文件
data_3['info']=ori_coco_ins['info']
# data_3['licenses']=ori_coco_ins['licenses']
data_3['categories']=ori_coco_ins['categories']
data_3['annotations']=[]
data_3['images']=[]

imgs = ori_coco_ins['images']
total_len = len(imgs)
split_r = 0.85


ann_ids =coco.getAnnIds()
img_ids = coco.getImgIds()
imgInfo = coco.imgs
annInfo = coco.anns

import numpy as np
np.random.seed(777)
img_ids=np.array(img_ids)
np.random.shuffle(img_ids)
line = int(total_len * split_r)
img_ids_train = img_ids[:line]
img_ids_val = img_ids[line:]


# for anno in annos:
#     print(anno)
#     w,h = anno['bbox'][2], anno['bbox'][3]
#     ratio = max(w/h, h/w)
#     if ratio<=12:
#         new_annos.append(anno)

train_images=[]
for id in img_ids_train:
    train_images.append(imgInfo[id])

ann_ids = coco.getAnnIds(imgIds= img_ids_train)
train_annos = coco.loadAnns(ids= ann_ids)

val_images=[]
for id in img_ids_val:
    val_images.append(imgInfo[id])

ann_ids = coco.getAnnIds(imgIds= img_ids_val)
val_annos = coco.loadAnns(ids = ann_ids)


# save_path = osp.pardir(ori_coco_json_path)
save_path = ori_coco_json_path = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\coco'

data_2['images'] = train_images
data_2['annotations'] = train_annos

data_3['images'] = val_images
data_3['annotations'] = val_annos


save_json_instance(osp.join(save_path, 'oneclass_12_train.json'), data_2)
save_json_instance(osp.join(save_path, 'oneclass_12_val.json'), data_3)