import json
import yaml
import pandas as pd
import os
import torch
from typing import Any, List, Optional, Tuple, Type, Union
import numpy as np
import cv2
#json yaml

def read_json_instance(abs_txt_name):
    with open(abs_txt_name, 'r', encoding='utf-8') as f: #读文件名
        ret_dic = json.load(f)
        return ret_dic

def save_json_instance(save_name, save):
    with open(save_name, 'w', encoding='utf-8') as f:
        # json.dump(save, f, ensure_ascii=False, indent=2)
        json.dump(save, f, ensure_ascii=False) #关掉indent省空间

        
def read_yaml_instance(name):
    return yaml.load(name)

def save_yaml_instance(save_name, save):
    with open(save_name, 'w') as file:
        file.write(yaml.dump(save, allow_unicode=True))

def dir_names(file_path):
    img_list = [x for x in os.listdir(file_path)]
    return img_list


def convert_overlay_heatmap(feat_map: Union[np.ndarray, torch.Tensor],
                            img: Optional[np.ndarray] = None,
                            alpha: float = 0.5) -> np.ndarray:
    """Convert feat_map to heatmap and overlay on image, if image is not None.

    Args:
        feat_map (np.ndarray, torch.Tensor): The feat_map to convert
            with of shape (H, W), where H is the image height and W is
            the image width.
        img (np.ndarray, optional): The origin image. The format
            should be RGB. Defaults to None.
        alpha (float): The transparency of featmap. Defaults to 0.5.

    Returns:
        np.ndarray: heatmap
    """
    assert feat_map.ndim == 2 or (feat_map.ndim == 3
                                  and feat_map.shape[0] in [1, 3])
    if isinstance(feat_map, torch.Tensor):
        feat_map = feat_map.detach().cpu().numpy()

    if feat_map.ndim == 3:
        feat_map = feat_map.transpose(1, 2, 0)

    norm_img = np.zeros(feat_map.shape)
    norm_img = cv2.normalize(feat_map, norm_img, 0, 255, cv2.NORM_MINMAX)
    norm_img = np.asarray(norm_img, dtype=np.uint8)
    heat_img = cv2.applyColorMap(norm_img, cv2.COLORMAP_JET)
    heat_img = cv2.cvtColor(heat_img, cv2.COLOR_BGR2RGB)
    if img is not None:
        heat_img = cv2.addWeighted(img, 1 - alpha, heat_img, alpha, 0) #叠加热力图
    return heat_img

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

def xyxy2xywh(box):
    x1 = min(box[0], box[2])
    y1 = min(box[1], box[3])
    w = abs(box[2]-box[0])
    h = abs(box[3]-box[1])
    return [x1, y1, w, h, w*h]

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

def gen_one_data_dict(img_name, h, w, id):
    data = {
        'file_name': os.path.basename(img_name),
        'height': h,
        'width': w,
        'id': id        
    }
    return data

def gen_one_anno_dict(cat_id, img_id, bbox: list, area, anno_id):
    anno = {
        'segmentation':[],
        'area': area, #直接取绝对值
        'iscrowd': 0,
        'image_id': img_id,
        'bbox': bbox,
        'category_id': cat_id,   
        'id': anno_id

    }
    return anno
    
def gen_category_dict(class_name):
    ins = []
    for k,v in enumerate(class_name):
        one_cate = {'id':k, 'name':v,'supercategory':v}
        ins.append(one_cate) 
    return ins

def read_txt(abs_txt_name):
    with open(abs_txt_name,'r', encoding='utf-8') as f:
        for line in f.readlines():
                line = line.replace(')','').replace('(','')
                row = line.strip().split(',')
                print(row)