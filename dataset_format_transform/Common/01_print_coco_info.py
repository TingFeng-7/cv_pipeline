import sys
sys.path.append(r'C:\Users\tingfeng-wu\Desktop\02_github\py_script\cocoapi\PythonAPI')
from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
from loguru import logger
import os


def coco_basic_info(data_root, dataType):
    annFile= os.path.join(data_root ,'coco', f'{dataType}.json' )
    # initialize COCO api for instance annotations
    coco=COCO(annFile)
    # coco_val=COCO(val_annFile)
    ann_ids =coco.getAnnIds()
    img_ids = coco.getImgIds()
    cat_id = coco.getCatIds()
    img2Ann = coco.imgToAnns
    imgInfo = coco.imgs
    logger.info(f'图片共有{len(img_ids)} 张, gt共有{len(ann_ids)}个')

def coco_basic_info1(annFile):
    coco=COCO(annFile)
    # coco_val=COCO(val_annFile)
    ann_ids =coco.getAnnIds()
    img_ids = coco.getImgIds()
    cat_ids = coco.getCatIds()
    # img2Ann = coco.imgToAnns
    imgInfo = coco.imgs
    # print(img_ids)
    print(f'图片共有{len(img_ids)} 张, gt共有{len(ann_ids)}个,平均一张图片有 {len(ann_ids)/len(img_ids)} 个gt')
    sum=0
    # 其实不需要顺序
    for v in imgInfo.items():
        #{1: {'file_name': '00001.jpg', 'height': 800, 'width': 800, 'id': 1} }
        ratio = v[1]['height'] / v[1]['width']
        sum+=ratio

    print(f'average {sum/len(imgInfo)}')
    cats = coco.loadCats(coco.getCatIds())
    nms=[cat['name'] for cat in cats]
    print(f'COCO categories: {nms}')
    # print('COCO categories: \n{}\n'.format(' '.join(nms)))
    min_det = 10 # id从1开始
    # print(min_det)
    max_det = 10
    max_id = 1
    for i in img_ids:
        cur_dt = coco.getAnnIds(imgIds=[i])
        min_det = min(min_det, len(cur_dt))
        max_id = i if len(cur_dt) > max_det else max_id
        max_det = max(max_det, len(cur_dt))
        
    for i in cat_ids: #按照类别统计 robust
        anns = coco.getAnnIds(catIds=i)
        # anns = coco.getAnnIds(catIds=i+1)
        print(f'{nms[i]} : {len(anns)}')


    print(f'min det:{min_det} max det:{max_det}')
    print(f'max id :{max_id} \nthe image contains max dets info:{imgInfo[max_id]}')
if __name__ =='__main__':
    data_root= r'D:\sa_data\sa_coco_1' #coco根目录
    trainType='train'
    # valType ='val'
    # coco_basic_info1(annFile = r'D:\sa_other\nv10-coco\annotations\train_en.json')
    # print('-'*80)
    # coco_basic_info1(annFile = r'D:\sa_other\nv10-coco\annotations\val_en.json')


    # #统计各个类别的gt数目是否平衡
    
    # coco_basic_info1(annFile = r'D:\sa_other\dior\annotations\DIOR_train.json')
    # print('-'*100)
    # coco_basic_info1(annFile = r'D:\sa_other\dior\annotations\DIOR_val.json')


    coco_basic_info1(annFile = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\coco\train.json')
    print('-'*100)
    coco_basic_info1(annFile = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\coco\val.json')