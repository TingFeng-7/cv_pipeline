import sys
sys.path.append(r'C:\Users\tingfeng-wu\Desktop\02_github\py_script')

from utils.utils1 import *
import os.path as osp

# json总共就两到三个文件
# 把category列改掉
# 把annotations的id们改掉
# ori_coco_json_path = r'D:\sa_data\0010_v1.5_filtered_linebox_yolox\coco\train_1class.json'
ori_coco_json_path = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\coco\val_v1.6.json'
ori_coco_json_path = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\coco\train_v1.6.json'
ori_coco_ins = read_json_instance(ori_coco_json_path)



annos = ori_coco_ins['annotations']

new_annos = []
from tqdm import tqdm
# annos = tqdm.tqdm(annos)
for anno in tqdm(annos):
    w,h = anno['bbox'][2], anno['bbox'][3]
    ratio = max(w/h, h/w)
    #只有linebox需要检查
    if anno['category_id'] == 2 and ratio >=22:
        continue
    else:
        new_annos.append(anno)
    
ori_coco_ins['annotations'] = new_annos
# save_path = osp.pardir(ori_coco_json_path)
save_path = ori_coco_json_path = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\coco'

save_json_instance(osp.join(save_path, 'train_22_v1.6.json'), ori_coco_ins)