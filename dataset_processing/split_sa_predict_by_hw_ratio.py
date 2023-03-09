from sympy import N
from utils import json_to_instance,instance_to_json,ensure_dir,Box  #不需要相对导入诶
import os
import glob
import sys
import shutil
from shutil import copyfile
from tqdm import tqdm

#用于总数据训练+分比例多数据集测试
#分开测试时，只看recall
#分开成labelme，后需要转成0001的sa

from loguru import logger

def split_by_HWr(json_file_path,bigHW_dir,norHW_dir,ratio=20):
    instancefrom = json_to_instance(json_file_path)
    instancefrom1 = json_to_instance(json_file_path)
    json_name = os.path.basename(json_file_path)
    logger.info(f'处理ing :{json_file_path}')
    bigHW_dir_json_to_path = os.sep.join([bigHW_dir, json_name])
    norHW_dir_json_to_path = os.sep.join([norHW_dir, json_name])
    bigHW = []
    norHW = []
    labels = ['text','icon','image','linebox']
    for label in labels:
        for shape in instancefrom[label]:
            try:
                p = shape['location']
                w = abs(p[2]-p[0])+1e-6
                h = abs(p[3]-p[1])+1e-6
                if h/w >= ratio or w/h >= 20:#宽高比大于20的话
                    continue
                if h/w >= ratio or (w/h >= 10 and w/h <= 20) :#宽高比大于20的话
                    bigHW.append(shape) 
                else:
                    norHW.append(shape)
            except:
                pass
        instancefrom[label] = bigHW
        instancefrom1[label] = norHW

    # instancefrom['shapes'] = bigHW
    instance_to_json(instancefrom, bigHW_dir_json_to_path)
    # instancefrom['shapes'] = norHW
    instance_to_json(instancefrom1, norHW_dir_json_to_path)
    
def split_by_HWr_3(json_file_path,bigHW_dir,norHW_dir,midHW_dir,ratio=20):
    instancefrom = json_to_instance(json_file_path)
    instancefrom1 = json_to_instance(json_file_path)
    instancefrom2 = json_to_instance(json_file_path)
    json_name = os.path.basename(json_file_path)
    logger.info(f'处理ing :{json_file_path}')
    bigHW_dir_json_to_path = os.sep.join([bigHW_dir, json_name])
    norHW_dir_json_to_path = os.sep.join([norHW_dir, json_name])
    midHW_dir_json_to_path = os.sep.join([midHW_dir, json_name])

    labels = ['text','icon','image','linebox']
    for label in labels:
        bigHW = []
        norHW = []
        midHW = []
        for shape in instancefrom[label]:
            try:
                p = shape['location']
                w = abs(p[2]-p[0])+1e-6
                h = abs(p[3]-p[1])+1e-6
                r = max(w/h ,h/w)
                if r >= 20:#宽高比大于20的话
                    bigHW.append(shape) 
                elif r>=10 :#宽高比大于20的话
                    midHW.append(shape) 
                else:
                    norHW.append(shape)
            except:
                pass
        instancefrom[label] = bigHW
        instancefrom1[label] = midHW
        instancefrom2[label] = norHW

    # instancefrom['shapes'] = bigHW
    instance_to_json(instancefrom, bigHW_dir_json_to_path)
    # instancefrom['shapes'] = norHW
    instance_to_json(instancefrom1, midHW_dir_json_to_path)
    instance_to_json(instancefrom2, norHW_dir_json_to_path)


if __name__ == '__main__':
    # root = r'D:\sa_1118'
    # 1.split gold_data
    # root = r'D:\sa_data\sa_coco_1'
    root = r'D:\sa_data\f36_exps\20221124_aware_hardnms_conf10_iou50\Element_grabbing\grabbing_evaluation\labelme' #
    # save_dir =  r'D:\sa_split'  
    save_dir =  r'D:\20221206_aware_hardnms_conf10_iou50\Element_grabbing\grabbing_evaluation' #

    test_folder_list = os.listdir(root)
    # test_folder_list =[os.listdir(root)]
    norHW_dirs = os.sep.join([save_dir,'smaller10_dir'])
    midHW_dirs =  os.sep.join([save_dir,'smaller20_dir'])
    bigHW_dirs =  os.sep.join([save_dir,'bigger20_dir'])
    for test_folder in test_folder_list:
        if test_folder !='grabbing_predict':
            continue
        bigHW_dir = os.sep.join([bigHW_dirs,test_folder])
        midHW_dir = os.sep.join([midHW_dirs,test_folder])
        norHW_dir = os.sep.join([norHW_dirs,test_folder])#gold_data
        ensure_dir(bigHW_dir)
        ensure_dir(norHW_dir)
        ensure_dir(midHW_dir)
        from01 = glob.glob(f'{root}/{test_folder}/*')
        print(test_folder)
        for json_file_path in from01:
            # split_by_HWr(json_file_path,bigHW_dir,norHW_dir,ratio=20)
            split_by_HWr_3(json_file_path,bigHW_dir,norHW_dir,midHW_dir,ratio=20)
 