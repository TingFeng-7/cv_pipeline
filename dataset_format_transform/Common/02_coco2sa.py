import sys
# sys.path.append(r'C:\Users\tingfeng-wu\Desktop\02_github\py_script\cocoapi\PythonAPI')
from pycocotools.coco import COCO
# 安装pycocotools 
import numpy as np
import skimage.io as io
from loguru import logger
import os

# xywh 2 xyxy
#每张图片
#未完成
# add score、自适应类别名
def save_result_sajson_auto(curr_image_bbox_class, curr_image_bboxes, scores, class_name, shape, name, save_folder):
    import json
    result_json={}
    #---
    result_json['imageName'] = name
    result_json['imgHeight'] = shape[0]
    result_json['imgWidth'] = shape[1]

    class_name_to_ids ={}
    for cls in class_name:
        result_json[cls] = []
    for k,v in enumerate(class_name):
        class_name_to_ids[v] = k
    # add
    for i in range(len(curr_image_bboxes)):
        cur_cls = curr_image_bbox_class[i]
        # cls_id = class_name_to_ids[cur_cls]
        if cur_cls == 'text':
            result_json[cur_cls].append({"location":curr_image_bboxes[i],'scores':scores[i], "content":''})
        else:
            result_json[cur_cls].append({"location":curr_image_bboxes[i], 'scores':scores[i]})
    os.makedirs(save_folder, exist_ok=True)#确定存在
    name = name[:-4] + '.json'
    json_name = os.path.join(save_folder, name)
    with open(json_name,'w', encoding='utf-8') as fw: 
        # json.dump(result_json, fw, indent=2)
        json.dump(result_json, fw)
        logger.info('{} saved'.format(json_name))

def save_result_SAjson(curr_image_bbox_class, curr_image_bboxes, shape, name, save_folder):
    # shape [h,w]
    import json
    result_json={}
    #---
    result_json['imageName'] = name
    result_json['imgHeight'] = shape[0]
    result_json['imgWidth'] = shape[1]
    #----
    boxes_text = []
    boxes_icon = []
    boxes_image = []
    boxes_linebox = []
    #--
    result_json['icon'] = []
    result_json['text'] = []
    result_json['image'] = []
    result_json['linebox'] = []
    # add
    for i in range(len(curr_image_bboxes)):
        if(curr_image_bbox_class[i] == 'icon'):
            boxes_icon.append({"location":curr_image_bboxes[i]}) 
        elif(curr_image_bbox_class[i] == 'text'):
            boxes_text.append({"location":curr_image_bboxes[i], "content":''})
        elif(curr_image_bbox_class[i] == 'image'):
            boxes_image.append({"location":curr_image_bboxes[i]})
        #add
        elif(curr_image_bbox_class[i] == 'linebox'):
            boxes_linebox.append({"location":curr_image_bboxes[i]})
            
    result_json['icon'] += boxes_icon
    result_json['text'] += boxes_text
    result_json['image'] += boxes_image
    result_json['linebox'] += boxes_linebox
    ##写入json
    os.makedirs(save_folder, exist_ok=True)#确定存在
    name = name[:-4] + '.json'
    json_name = os.path.join(save_folder, name)
    with open(json_name,'w', encoding='utf-8') as fw: 
        json.dump(result_json, fw, indent=2)
        logger.info('{} saved'.format(json_name))

if __name__ =='__main__':
    data_root= r'D:\sa_data\0010_v1.5_filtered_linebox_yolox' #coco根目录
    trainType='train'
    valType ='val'
    annFile= os.path.join(data_root ,'coco', f'{trainType}.json' )
    val_annFile = os.path.join(data_root ,'coco', f'{valType}.json' )
    # initialize COCO api for instance annotations
    coco=COCO(annFile)
    # coco_val=COCO(val_annFile)
    ann_ids =coco.getAnnIds()
    img_ids = coco.getImgIds()#5644
    cat_id = coco.getCatIds()
    print(coco.cats)
    img2Ann = coco.imgToAnns
    imgInfo = coco.imgs
    new_save_folder = os.path.join(data_root, './coco2SAcomps')
    os.makedirs(new_save_folder,exist_ok=True)
    catid2name = coco.cats
    for i in range(len(imgInfo)):
        hw = [imgInfo[i+1]['height'], imgInfo[i+1]['width']]
        name = imgInfo[i+1]['file_name']
        per_img_anno = img2Ann[i+1]
        bbox_len = len(per_img_anno)
        currbox =[]
        currcls=[]
        for v in per_img_anno:
            #swap
            x,y,w,h = v['bbox']
            x2 = x+w
            y2 = y+h
            # if(v['bbox'][0] >v['bbox'][2]):
            #     tmp = v['bbox'][0]
            #     v['bbox'][0] = v['bbox'][2]
            #     v['bbox'][2] = tmp
            currbox.append([x,y,x2,y2])
            currcls.append(catid2name[v['category_id']]['name'])
        save_result_SAjson(currcls, currbox, hw, name, new_save_folder)