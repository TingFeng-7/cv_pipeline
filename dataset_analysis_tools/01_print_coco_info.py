# import sys
# sys.path.append(r'E:\A01_cyclone\02_github\py_script\cocoapi\PythonAPI')
from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
from loguru import logger
import os
import numpy as np
import csv

#借助cocoapi 来看这个原图尺寸的

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

def caculate_wh_maxratio(w, h): #最大长宽比
    return max(w/h, h/w)

def caculate_ratio(a, b):
    return a/b

def coco_basic_info_plus(annFile):
    coco=COCO(annFile)
    # coco_val=COCO(val_annFile)
    ann_ids =coco.getAnnIds()
    img_ids = coco.getImgIds()
    cat_ids = coco.getCatIds()
    img2Ann = coco.imgToAnns
    imgInfo = coco.imgs
    print(f'图片共有{len(img_ids)} 张, \ngt共有{len(ann_ids)}个\nper image have {len(ann_ids)/len(img_ids)} 个gt')
    sum=0
    # 每张图片的长宽比
    for v in imgInfo.items():
        #{1: {'file_name': '00001.jpg', 'height': 800, 'width': 800, 'id': 1} }
        ratio = v[1]['height'] / v[1]['width']
        sum+=ratio
    print(f'average 长宽比 of images : {sum/len(imgInfo)}')
    cats = coco.loadCats(coco.getCatIds())
    nms=[cat['name'] for cat in cats]
    print(f'COCO categories: {nms} totally {len(nms)}')
    # print('COCO categories: \n{}\n'.format(' '.join(nms)))
    min_det = 100 #  id从1开始
    # print(min_det)
    max_det = 10
    max_id = 1
    for i in img_ids:
        cur_det = coco.getAnnIds(imgIds=[i])
        min_det = min(min_det, len(cur_det))
        max_id = i if len(cur_det) > max_det else max_id
        max_det = max(max_det, len(cur_det)) #当前最大框
    bbox_ratios_dicts = {}

    for i in cat_ids: #按照类别统计 robust
        anns_id = coco.getAnnIds(catIds=i) #获取id
        anns_dict = coco.loadAnns(ids = anns_id)
        cur_cls_name = nms[i]
        print('*'*100)
        print(f'{cur_cls_name} : {len(anns_id)}')
        # 统计长宽比
        bbox_ratios_dicts[cur_cls_name+'_bbox_ratio'] = []
        ratio1 = []
        abs_ratio=[]
        for ann in anns_dict:
            bbox, area = ann['bbox'], ann['area']
            w,h = bbox[2],bbox[3]
            if w==0 or h==0: continue
            # 1. h > w
            # if(bbox[3]>bbox[2]): 
            #     h_div_w_ratio.append(caculate_ratio(bbox[3], bbox[2]))
            # # 2. w > h
            # else: 
            #     w_div_h_ratio.append(caculate_ratio(bbox[2], bbox[3]))
            # ratio1.append(caculate_wh_maxratio(bbox[3], bbox[2]))
            ratio1.append(caculate_ratio(bbox[2], bbox[3]))

        # print('1. max_ratio')
        # save_wh_ratio(ratio1, cur_cls_name+'_ratio1.csv')
        # print('>'*100)
        # print('2. height / width')
        # save_wh_ratio(h_div_w_ratio, cur_cls_name+'_ratio2.csv')
        # print('>'*100)
        # print('3. width / height')
        # save_wh_ratio(w_div_h_ratio,cur_cls_name+'_ratio3.csv')
        # print('<'*100)
        # print('4. w / h')
        # save_wh_ratio(abs_ratio,cur_cls_name+'_ratio4.csv')
    
    print(f'min det: {min_det} max det: {max_det}')
    print(f'max id : {max_id} \n the maxdets Imginfo: {imgInfo[max_id]}')

def save_wh_ratio(arry, csvname):
    arry = np.array(arry)
    parms = [25,50,75,90,95,98,99,99.5]
    percent_nums ={}
    save_to_csv(arry, csvname, parms, percent_nums)
    import json
    print(json.dumps(percent_nums,indent=2))

def save_to_csv(arry, csvname, parms, percent_nums):
    csv_file = open(csvname, 'w', newline='', encoding='utf-8')
    # 调用open()函数打开csv文件，传入参数：文件名“demo.csv”、写入模式“w”、newline=''、encoding='gbk'
    writer = csv.writer(csv_file)
    for parm in parms:
        try:
            percent_nums[str(parm)+'%'] = np.percentile(arry, parm)
            writer.writerow([str(parm)+'%', np.percentile(arry, parm)])
        # 调用writer对象的writerow()方法，可以在csv文件里写入一行文字 “电影”和“豆瓣评分”。
        # writer.writerow(['喜羊羊与灰太狼', '9.9'])
        except:
            pass
    csv_file.close()

def save_to_csv_ncols(arry, csvname, parms, percent_nums):
    csv_file = open(csvname, 'w', newline='', encoding='utf-8')
    # 调用open()函数打开csv文件，传入参数：文件名“demo.csv”、写入模式“w”、newline=''、encoding='gbk'
    writer = csv.writer(csv_file)
    header_list = [str(parm)+'%' for parm in parms]
    writer.writerow(header_list)
    data_list = []
    for parm in parms:
        try:
            percent_nums[str(parm)+'%'] = np.percentile(arry, parm)
            data_list.append(np.percentile(arry, parm))
        # 调用writer对象的writerow()方法，可以在csv文件里写入一行文字 “电影”和“豆瓣评分”。
        except:
            data_list.append(0)
        writer.writerow(data_list)
    csv_file.close()

if __name__ =='__main__':
    data_root= '/data/visDrone20191/visdrone2019-yolo' #coco根目录

    # coco_basic_info_plus(annFile = r'D:\sa_other\nv10-coco\annotations\train_en.json')
    # print('-'*80)
    # coco_basic_info_plus(annFile = r'D:\sa_other\nv10-coco\annotations\val_en.json')


    # #统计各个类别的gt数目是否平衡
    # coco_basic_info_plus(annFile = r'D:\sa_other\dior\annotations\DIOR_train.json')
    # print('-'*100)
    # coco_basic_info_plus(annFile = r'D:\sa_other\dior\annotations\DIOR_val.json')

    # print('-'*100)
    # os.chdir(r'E:\visDrone2019')
    from os.path import join as opj
    coco_basic_info_plus(annFile = opj(data_root,'train.json'))
    print('-'*100)
    coco_basic_info_plus(annFile = opj(data_root,'val.json'))



# 关闭文件
