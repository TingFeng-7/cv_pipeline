from asyncio.log import logger
from cProfile import label
from turtle import shape
import cv2
import numpy as np
import os
import json
from .colors import _COLORS

def vis_based_json(img :cv2.Mat , boxes: list, cls_ids: dict, labels: list) -> cv2.Mat : #预测的id ，预测的类别字典
    '''
    boxes: [left top - right bottom]
    '''
    # shape_list = []
    for i in range(len(boxes)):
        box = boxes[i]
        # cls_id = int(cls_ids[i])
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])
        ## box位置 和 label 左上角和右下角
        # print(labels[i])
        cls_id = cls_ids[labels[i]]
        color = (_COLORS[cls_id] * 255).astype(np.uint8).tolist()
        text = '{}%'.format(labels[i]) #输出类名即可
        txt_color = (0, 0, 0) if np.mean(_COLORS[cls_id]) > 0.5 else (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX

        txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
        cv2.rectangle(img, (x0, y0), (x1, y1), color, 2)

        txt_bk_color = (_COLORS[cls_id] * 255 * 0.7).astype(np.uint8).tolist()
        cv2.rectangle(
            img,
            (x0, y0 + 1),
            (x0 + txt_size[0] + 1, y0 + int(1.5*txt_size[1])),
            txt_bk_color,
            -1
        )
        cv2.putText(img, text, (x0, y0 + txt_size[1]), font, \
                    0.4, txt_color, thickness=1)
    return img

def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder
## 方法部分




if __name__ == '__main__':
    # import cv2
    root = r'D:\sa_data\exps\2022.10.8_htx_dbnet\Element_grabbing\grabbing_evaluation' #图片目录
    label_dir = r'D:\sa_data\exps\20221026_yolox-nano_conf_0.2\Element_grabbing\grabbing_evaluation' #保存结果的目录
    imgs_link = r'imgs'
    predic_link = r'yolox_predict'

    #-----1.以上是路径
    app_names = os.listdir(root) 
    app_names = [x for x in app_names if x < "0028"]
    class_names = ['text','icon','image']  #

    cls_ids ={} # text：0
    for k,v in enumerate(class_names):
        cls_ids[v] = k


    # print(cls_ids)
    from loguru import logger
    #-----2.以上是类别名的处理
    for app in app_names:
        app_folder = os.path.join(root, app) #app 文件夹
        if (label_dir == ''): #不设置预测结果的路径的话，默认在一起
            predict_debug_folder = os.path.join(app_folder, 'predict_debug')
            predict_folder = os.path.join(app_folder, predic_link)

        else:
            label_folder = os.path.join(label_dir, app)
            predict_debug_folder = os.path.join(label_folder, 'predict_debug')
            predict_folder = os.path.join(label_folder, predic_link)
        
        img_folder = os.path.join(app_folder, imgs_link)
        logger.info("画出的bbox框图片将保存在: {}".format(predict_debug_folder))
        ensure_dir(predict_debug_folder)
        
        for item in os.listdir(img_folder): #每一张照片
            img_name = os.path.join(img_folder, item)
            json_path = os.path.join(predict_folder, item[:-4] +'.json') 
            img = cv2.imread(img_name)
            with open(json_path, "r", encoding='utf-8') as f:
                gt = json.load(f) #所有内容
                #wtf add
                bbox_list=[]
                label_list =[]
                for cn in class_names: #每一张照片里的
                    try:
                        cn_bbox_list = [x["location"] for x in gt[cn]]
                        bbox_list += cn_bbox_list
                        label_list += [cn for x in gt[cn]]
                    except:
                        continue #没有这类直接继续
                # print(label_list)
                gt_img = vis_based_json(img, bbox_list, cls_ids, label_list)
                # gt_img = draw(img, gt) 普通版本
                print("正在处理"+img_name)
                savepath = os.path.join(predict_debug_folder,item+'_draw_predict'+'.png')
                # savepath = os.sep.join([predict_debug_folder,item+'_draw_predict'+'.png'])
                print("save path:"+savepath)
                cv2.imwrite(savepath,gt_img)