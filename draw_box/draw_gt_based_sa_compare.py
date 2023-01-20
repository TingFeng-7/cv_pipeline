#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii Inc. All rights reserved.
from asyncio.log import logger
import cv2
import numpy as np
import os
import json
from tqdm import tqdm

#预测的id ，预测的类别字典 画框不限类别
def vis_based_json(img :cv2.Mat , boxes: list,labels: list, cls_ids: dict) -> cv2.Mat : 
    # shape_list = []
    for i in range(len(boxes)):
        box = boxes[i]
        # cls_id = int(cls_ids[i])
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])
        ## box位置 和 label 左上角和右下角
        # 只要linebox
        # if(labels[i] != 'linebox'):
        #     continue
        cls_id = cls_ids[labels[i]] * 3 #让颜色跳跃下

        color = (_COLORS[cls_id] * 255).astype(np.uint8).tolist()#看id是几号颜色 就是多少
        text = '{}'.format(labels[i]) #输出类名即可
        txt_color = (0, 0, 0) if np.mean(_COLORS[cls_id]) > 0.5 else (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX

        txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
        cv2.rectangle(img, (x0, y0), (x1, y1), color, thickness=1)
        # 是否背景+文字
        txt_bk_color = (_COLORS[cls_id] * 255 * 0.7).astype(np.uint8).tolist()
        if (cls_id/3 == 0):
            cv2.rectangle(img,(x0, y0 + 1),(x0 + txt_size[0] + 1, y0 + int(1.5*txt_size[1])),txt_bk_color,-1)#背景框
            cv2.putText(img, text, (x0, y0 + txt_size[1]), font, 0.4, txt_color, thickness=1)
        else:## i=2
            cv2.rectangle(img,(x0, y1),(x0 + txt_size[0] + 1, y1 - int(1.5*txt_size[1])),txt_bk_color,-1)
            cv2.putText(img, text, (x0, y1 - int(0.5*txt_size[1])), font, 0.4, txt_color, thickness=1)
    return img

def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

#类别限制
def draw(img :cv2.Mat, label, class_names):
    icon_locs = [x["location"] for x in label['icon']]
    text_locs = [x["location"] for x in label['text']]#键值可以是变量
    for loc in icon_locs:
        x1,y1,x2,y2 = loc[0], loc[1], loc[2], loc[3]
        points = [(int(x1),int(y1)),(int(x2),int(y2))] #左上和右下
        cv2.rectangle(img,points[0],points[1],(0,0,250),1)#绘出矩形框
    for loc in text_locs:
        x1,y1,x2,y2 = loc[0], loc[1], loc[2], loc[3]
        points = [(int(x1),int(y1)),(int(x2),int(y2))] #左上和右下
        cv2.rectangle(img,points[0],points[1],(0,250,),1)#绘出矩形框
    bbox_list=[]
    cls_id =[]
    for cn in class_names:
        cn_bbox_list = [x["location"] for x in label[cn]]
        bbox_list += cn_bbox_list
        cls_id.append(cls_id[class_names])
    return img

## 方法部分

_COLORS = np.array(
    [
        0.000, 0.447, 0.741,
        0.850, 0.325, 0.098,
        0.929, 0.694, 0.125,
        0.494, 0.184, 0.556,
        0.466, 0.674, 0.188,
        0.301, 0.745, 0.933,
        0.635, 0.078, 0.184,
        0.300, 0.300, 0.300,
        0.600, 0.600, 0.600,
        1.000, 0.000, 0.000,
        1.000, 0.500, 0.000,
        0.749, 0.749, 0.000,
        0.000, 1.000, 0.000,
        0.000, 0.000, 1.000,
        0.667, 0.000, 1.000,
        0.333, 0.333, 0.000,
        0.333, 0.667, 0.000,
        0.333, 1.000, 0.000,
        0.667, 0.333, 0.000,
        0.667, 0.667, 0.000,
        0.667, 1.000, 0.000,
        1.000, 0.333, 0.000,
        1.000, 0.667, 0.000,
        1.000, 1.000, 0.000,
        0.000, 0.333, 0.500,
        0.000, 0.667, 0.500,
        0.000, 1.000, 0.500,
        0.333, 0.000, 0.500,
        0.333, 0.333, 0.500,
        0.333, 0.667, 0.500,
        0.333, 1.000, 0.500,
        0.667, 0.000, 0.500,
        0.667, 0.333, 0.500,
        0.667, 0.667, 0.500,
        0.667, 1.000, 0.500,
        1.000, 0.000, 0.500,
        1.000, 0.333, 0.500,
        1.000, 0.667, 0.500,
        1.000, 1.000, 0.500,
        0.000, 0.333, 1.000,
        0.000, 0.667, 1.000,
        0.000, 1.000, 1.000,
        0.333, 0.000, 1.000,
        0.333, 0.333, 1.000,
        0.333, 0.667, 1.000,
        0.333, 1.000, 1.000,
        0.667, 0.000, 1.000,
        0.667, 0.333, 1.000,
        0.667, 0.667, 1.000,
        0.667, 1.000, 1.000,
        1.000, 0.000, 1.000,
        1.000, 0.333, 1.000,
        1.000, 0.667, 1.000,
        0.333, 0.000, 0.000,
        0.500, 0.000, 0.000,
        0.667, 0.000, 0.000,
        0.833, 0.000, 0.000,
        1.000, 0.000, 0.000,
        0.000, 0.167, 0.000,
        0.000, 0.333, 0.000,
        0.000, 0.500, 0.000,
        0.000, 0.667, 0.000,
        0.000, 0.833, 0.000,
        0.000, 1.000, 0.000,
        0.000, 0.000, 0.167,
        0.000, 0.000, 0.333,
        0.000, 0.000, 0.500,
        0.000, 0.000, 0.667,
        0.000, 0.000, 0.833,
        0.000, 0.000, 1.000,
        0.000, 0.000, 0.000,
        0.143, 0.143, 0.143,
        0.286, 0.286, 0.286,
        0.429, 0.429, 0.429,
        0.571, 0.571, 0.571,
        0.714, 0.714, 0.714,
        0.857, 0.857, 0.857,
        0.000, 0.447, 0.741,
        0.314, 0.717, 0.741,
        0.50, 0.5, 0
    ]
).astype(np.float32).reshape(-1, 3)

def json_to_instance(json_file_path: str):
    '''
    :param json_file_path: json文件路径
    :return: json instance
    '''
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    return instance

if __name__ == '__main__':
    # import cv2
    img_root_dir = r'D:\sa_data\0010_v1.5_filtered_linebox_yolox' #图片根目录 
    # img_root_dir = r'D:\sa_split_32'
    #图片位置和json位置。1.图片＋gold_data 2.图片+预测json
    # label_dir = 'gold'
    # label_dir = r'D:\sa_split_32\20221124_aware_hardnms_conf10_iou60\Element_grabbing\grabbing_evaluation' #预测json目录
    imgs_link = r'imgs'
    predict_rootdir = r'C:\Users\tingfeng-wu\Desktop\20221226_yolox-nano-fpn4\Element_grabbing\grabbing_evaluation'
    # predict_link = r'comps'
    predict_link = r'grabbing_predict'
    #--1.以上是路径
    app_names = os.listdir(img_root_dir)
    # app_names = os.listdir(r'D:\sa_split_32')
    # app_names = [x for x in app_names]
    app_names = [x for x in app_names if x =='labelme']
    print(app_names)
    
    # class_names = ['text','icon','image','linebox']  #
    class_names = ['linebox']
    classes = ['linebox_gt','linebox_dt']
    cls_ids ={} # text：0
    for k,v in enumerate(classes):
        cls_ids[v] = k
    debug_name = 'imgswithcompares'
    # debug_name = 'linebox_debug'
    from loguru import logger
    #--2.以上是类别名的处理
    for app in app_names:
        app_folder = os.path.join(img_root_dir, app) #app 文件夹

        label_folder = os.path.join(predict_rootdir, app)#预测标签的位置
        predict_debug_folder = os.path.join(label_folder, debug_name)
        predict_folder = os.path.join(label_folder, 'grabbing_predict')
        
        img_folder = os.path.join(app_folder, imgs_link) #gold_data
        gold_data_folder = os.path.join(app_folder, 'comps')
        
        logger.info("画出的bbox框图片将保存在: {}".format(predict_debug_folder))
        ensure_dir(predict_debug_folder)
        imgs_name = [x for x in os.listdir(img_folder) if x.endswith('png')]
        for item in tqdm(imgs_name): #每一张照片
            img_name = os.path.join(img_folder, item)
            dt_json_path = os.path.join(predict_folder, item[:-4] +'.json') 
            gt_json_path = os.path.join(gold_data_folder, item[:-4] +'.json') 
            dt = json_to_instance(dt_json_path)
            gt = json_to_instance(gt_json_path)
            img = cv2.imread(img_name)
            # with open(json_path, "r", encoding='utf-8') as f:
            #     gt = json.load(f) #所有内容
            #wtf add
            bbox_list=[]
            label_list =[]
            for cn in class_names: #每一张照片里的标签
                try:
                    # cn_bbox_list = [x["location"] for x in gt[cn]]
                    bbox_list += [x["location"] for x in gt[cn]]
                    bbox_list += [x["location"] for x in dt[cn]]
                    label_list += [cn+'_gt' for x in gt[cn]]
                    label_list += [cn+'_dt' for x in dt[cn]]
                except:
                    continue #没有这类直接继续

            gt_img = vis_based_json(img, bbox_list, label_list, cls_ids)

            # print("正在处理"+img_name)
            savepath = os.path.join(predict_debug_folder,item+'_draw_predict'+'.png')
            # savepath = os.sep.join([predict_debug_folder,item+'_draw_predict'+'.png'])
            # print("save path:"+ savepath)
            cv2.imwrite(savepath, gt_img)