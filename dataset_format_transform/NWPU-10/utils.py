# -*- coding: UTF-8 -*-
import json
import os
from os.path import join as pathj
import datetime
# from loguru import logger
from PIL import Image
import cv2


def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def line2str(l):
    str1 = ''
    for ele in l[0:-1]:
        str1 = str1 + str(ele)+' '
    return str1 + str(l[-1])


def gen_class2id(classes):
    cls2id = {}
    for k, v in enumerate(classes):
        cls2id[v] = k
    return cls2id


def xyxy2cxcy(box):
    cx = (box[0]+box[2]) * 0.5
    cy = (box[1]+box[3]) * 0.5
    w = abs(box[2]-box[0])
    h = abs(box[3] - box[1])
    return [cx, cy, w, h, w*h]


class gen_COCO:
    def gen_empty_cocojson_instance():
        # 创建 总标签data
        now = datetime.datetime.now()
        instance = dict(
            info=dict(
                description=None,
                url=None,
                version=None,
                year=now.year,
                contributor=None,
                date_created=now.strftime("%Y-%m-%d %H:%M:%S.%f"),
            ),
            licenses=[dict(url=None, id=0, name=None,)],
            images=[
                # license, url, file_name, height, width, date_captured, id
            ],
            type="instances",
            annotations=[
                # segmentation, area, iscrowd, image_id, bbox, category_id, id
            ],
            categories=[
                # supercategory, id, name
            ],
        )

        return instance

    def gen_one_data_dict(img_name, h, w,  id):
        data = {
            'file_name': os.path.basename(img_name),
            'height': h,
            'width': w,
            'id': id
        }
        return data

    def gen_one_anno_dict(cat_id, img_id, bbox: list, area, anno_id):
        anno = {
            'segmentation': [],
            'area': area,  # 直接取绝对值
            'iscrowd': 0,
            'image_id': img_id,
            'bbox': bbox,
            'category_id': cat_id,
            'id': anno_id

        }
        return anno

    def gen_category_dict(class_name):
        ins = []
        for k, v in enumerate(class_name):
            one_cate = {'id': k+1, 'name': v, 'supercategory': v}
            ins.append(one_cate)
        return ins

def gen_empty_labelmejson_instance():
    # 创建 总标签data
    instance = dict(
        version="5.0.1",
        flags={},
        shapes=[],
        imagePath='',
        imageData=None,
        imageHeight=0,
        imageHeight=0,
    )
    return instance

class gen_Labelme:
    def __init__(self, label_file=None):
        if label_file is None:
            self.labelme_json = gen_empty_labelmejson_instance()
        else:
            raise Exception("label_file type error")



    def set_info(self, img_path, img):
        h, w = img.shape[:2]
        self.labelme_json["imagePath"] = img_path
        self.labelme_json["imageWidth"] = w
        self.labelme_json["imageHeight"] = h
        return self.labelme_json

    def gen_one_shape_dict(label_name, bbox: list):
        data = {
            "label": label_name,
            "point": [[bbox[0],bbox[2]], [bbox[1], bbox[3]]],
            'group_id': None,
            'shape_type': "rectangle",
            'flags':{}
        }
        return data



def read_txt(abs_txt_name):
    with open(abs_txt_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.replace(')', '').replace('(', '')
            row = line.strip().split(',')
            print(row)
# load json


def read_json(abs_txt_name):
    with open(abs_txt_name, 'r', encoding='utf-8') as f:  # 读文件名
        ret_dic = json.load(f)
        return ret_dic


def save_json(new_name, json_ins):
    with open(new_name, 'w', encoding='utf-8') as f:
        json.dump(json_ins, f, indent=2, ensure_ascii=False)  # zw
        print('{} saved'.format(new_name))
