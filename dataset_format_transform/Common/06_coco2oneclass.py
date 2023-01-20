import sys
sys.path.append(r'C:\Users\tingfeng-wu\Desktop\02_github\py_script')

from utils.utils1 import *
import os.path as osp

# json总共就两到三个文件
# 把category列改掉
# 把annotations的id们改掉
def gen_category_part(class_name):
    ins = []
    for k,v in enumerate(class_name):
        one_cate = {'id':k, 'name':v,'supercategory':v}
        ins.append(one_cate) 
    return ins

ori_coco_json_path = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\coco\train_v1.7.json'
# ori_coco_json_path = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\coco\val_v1.7.json'
ori_coco_ins = read_json_instance(ori_coco_json_path)
cls_name=['linebox','v_line','h_line']

new_cate = gen_category_part(cls_name)
ori_coco_ins['categories'] = new_cate



annos = ori_coco_ins['annotations']
import tqdm
new_annos=[]
for anno in annos:
    if anno['category_id'] == 1:
        w,h = anno['bbox'][2:]
        if w>h:
            anno['category_id'] = 2
        new_annos.append(anno)
    else:
        new_annos.append(anno)

    
    
ori_coco_ins['annotations'] = annos
ori_coco_ins['categories'] = new_cate
# save_path = osp.pardir(ori_coco_json_path)
save_path = ori_coco_json_path = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\coco'

save_json_instance(osp.join(save_path, 'train_v1.8.json'), ori_coco_ins)