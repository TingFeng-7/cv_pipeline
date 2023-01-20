import os
import os.path as osp
import sys
import cv2
import albumentations as A
import albumentations.augmentations.geometric.resize as are
# img_path = 'D:/PythonProject/UWGAN_UIE-master/UNetRestoration/data/water/'
# gt_path = 'D:/PythonProject/UWGAN_UIE-master/UNetRestoration/data/gt/'
import json
import numpy as np
# save
def gen_empty_labelmejson_instance():
    # 创建 总标签data
    instance = dict(
        version="5.0.1",
        flags={},
        shapes=[],
        imagePath='',
        imageData=None,
        imageHeight = 0,
        imageWidth = 0
    )
    return instance

def gen_one_shape_dict(bbox: list, label_name):
    data = {
        "label": label_name,
        "points": [[bbox[0],bbox[2]], [bbox[1], bbox[3]]],# ! [xmin ymin xmax ymax]
        'group_id': None,
        'shape_type': "rectangle",
        'flags':{}
    }
    # shape = dict(
    #     label_name = label_name,

    # )
    return data

def gen_shapes_instance(bboxes_list, labels_list):
    # 创建 总标签data
    shapes_ins = []
    bboxes_list = xywh2xyxy(bboxes_list)
    for i,bbox in enumerate(bboxes_list):
        # xyxy transform [xmin ymin w, h]

        per_bbox = gen_one_shape_dict(bbox, labels_list[i])
        shapes_ins.append(per_bbox)
    return shapes_ins

# img_path = 'images/000000386298.jpg'
# image = cv2.imread('images/000000386298.jpg')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# bboxes = [[5.66, 138.95, 147.09, 164.88], [366.7, 80.84, 132.8, 181.84]]
# category_ids = [17, 18]
# # We will use the mapping from category_id to the class name
# # to visualize the class label for the bounding box on the image
# category_id_to_name = {17: 'cat', 18: 'dog'}

import torch
def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[:, 0] = x[:, 0]
    y[:, 1] = x[:, 1]
    y[:, 2] = x[:, 0] + x[:, 2]  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3]  # bottom right y
    return y

def set_info(ins, img_path, img):
    h, w = img.shape[:2]
    ins["imagePath"] = img_path
    ins["imageWidth"] = w
    ins["imageHeight"] = h
    return ins

# ins = set_info(ins, img_path, image)
# load

def read_path(file_path, gt_path, save_dir):
    #遍历该目录下的所有图片文件
    os.makedirs(save_dir, exist_ok=True)
    img_list = dir_names(file_path)
    for filename in img_list:
        #print(filename)
        json_filename = filename[:filename.rfind('.')]+'.json'
        img_name = osp.join(file_path, filename)
        gt_name = osp.join(gt_path, json_filename)

        img = cv2.imread(img_name)
        bboxes, labels = extract_bboxes_from_labelme(gt_name, img)
        # new_image = cv2.resize(img, (1366, 768), interpolation=cv2.INTER_AREA) #缩小
        # new_image = cv2.pyrDown(img, (1280,720))
        # new_image = are.LongestMaxSize(img, max_size=1280)
        ## albu transform
        transform = A.Compose(
            [A.HorizontalFlip(p=0.5),
            A.augmentations.geometric.resize.LongestMaxSize(max_size=1280)],
            # bbox_params=A.BboxParams(format='coco', label_fields=['category_ids']),
            bbox_params=A.BboxParams(format='pascal_voc', label_fields=['class_labels']),
        )
        # random.seed(7)
        # 解析拿到所有 bbox 和 label
        transformed = transform(image=img, bboxes=bboxes, class_labels= labels) #! 可以bbox with label

        new_bboxes = transformed['bboxes']
        new_bboxes = [list(x) for x in new_bboxes]
        new_bboxes = np.array(new_bboxes)
        new_image = transformed['image']

        cv2.imwrite(osp.join(save_dir, filename), new_image)

        ins = gen_empty_labelmejson_instance()
        ins = set_info(ins, filename, new_image)
        # new_bboxes = np.array(new_bboxes)
        ins['shapes'] = gen_shapes_instance(new_bboxes, labels)
        save_json(osp.join(save_dir, json_filename), ins)

def extract_bboxes_from_labelme(gt_name, img):
    labelme_gt = read_json(gt_name)
    h, w = img.shape[:2]
    bboxes = []
    labels = []
    for bbox in labelme_gt["shapes"]:
        if len(bbox["points"]) < 2:
            continue
        try:
            [xmin, ymin], [xmax, ymax] = bbox["points"] #左下 右上
        except:
            pass
        b = [int(float(xmin)), int(float(ymin)), int(float(xmax)),
        int(float(ymax))]
        if (b[3] - b[1] <= 0) or (b[2] - b[0] <= 0) or (b[3]>h) or(b[2]>w):
            print("error rect:", b)
            continue
        bboxes.append([bbox['points'][0][0], bbox['points'][0][1], \
                bbox['points'][1][0], bbox['points'][1][1]])
        labels.append(bbox["label"])
    return bboxes,labels

def dir_names(file_path):
    img_list = [x for x in os.listdir(file_path)]
    return img_list

# 读取json
def read_json(abs_txt_name):
    with open(abs_txt_name, 'r', encoding='utf-8') as f: #读文件名
        ret_dic = json.load(f)
        return ret_dic
        
def save_json(new_name,json_ins):
    with open(new_name, 'w',encoding='utf-8') as f:
        json.dump(json_ins ,f ,indent=2,ensure_ascii=False)#zw
        print('{} saved'.format(new_name)) 

if __name__ == '__main__':

    img_path = r'D:\sa_data\0006_sa_v1.6_cleanto_0010\0001_cyclone_1.5\imgs'
    gt_path = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\labelme'
    save_dir = r'C:\Users\tingfeng-wu\Desktop\02_github\labelme_6401'

    read_path(img_path, gt_path, save_dir)