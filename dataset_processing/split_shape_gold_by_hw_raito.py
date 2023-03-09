from sympy import N
from utils import json_to_instance,instance_to_json,ensure_dir,Box
import os
import glob
import sys
import shutil
from shutil import copyfile
from tqdm import tqdm
from loguru import logger
import json
#用于总数据训练+分比例多数据集测试
#分开测试时，只看recall
#分开成labelme，后需要转成0001的sa

def split_by_HWr(json_file_path,bigHW_dir,norHW_dir, ratio=20):
    instancefrom = json_to_instance(json_file_path)
    json_name = os.path.basename(json_file_path)
    bigHW_dir_json_to_path = os.sep.join([bigHW_dir, json_name])
    norHW_dir_json_to_path = os.sep.join([norHW_dir, json_name])
    bigHW = []
    norHW = []
    for shape in instancefrom['shapes']:
        try:
            p = shape['points']
            w = abs(p[1][0]-p[0][0])+1e-6
            h = abs(p[1][1]-p[0][1])+1e-6
            if h/w >= ratio or w/h >= ratio:#宽高比大于10的话
                bigHW.append(shape) 
            else:
                norHW.append(shape)
        except:
            pass
    instancefrom['shapes'] = bigHW
    instance_to_json(instancefrom, bigHW_dir_json_to_path)
    instancefrom['shapes'] = norHW
    instance_to_json(instancefrom, norHW_dir_json_to_path)


def split_by_HWr_3(json_file_path, bigHW_dir, norHW_dir, midHW_dir, ratio=20):
    instancefrom = json_to_instance(json_file_path)
    json_name = os.path.basename(json_file_path)
    bigHW_dir_json_to_path = os.sep.join([bigHW_dir, json_name])
    midHW_dir_json_to_path = os.sep.join([midHW_dir, json_name])
    norHW_dir_json_to_path = os.sep.join([norHW_dir, json_name])
    bigHW = []
    norHW = []
    midHW = []
    for shape in instancefrom['shapes']:
        try:
            p = shape['points']
            w = abs(p[1][0]-p[0][0])+1e-6
            h = abs(p[1][1]-p[0][1])+1e-6
            r = max(h/w, w/h)

            if r>= ratio:#宽高比大于20的话
                bigHW.append(shape) 
            elif r>=10:
                print('>10 and <20')
                midHW.append(shape)
            else:
                norHW.append(shape)
        except:
            pass
    instancefrom['shapes'] = bigHW
    instance_to_json(instancefrom, bigHW_dir_json_to_path)
    instancefrom['shapes'] = norHW
    instance_to_json(instancefrom, norHW_dir_json_to_path)
    instancefrom['shapes'] = midHW
    instance_to_json(instancefrom, midHW_dir_json_to_path)
    
def parse_labelme_json_autoScale(file_path, cls_name, image_path=""):
    annos = {}
    boxes_dict = {}
    for name in cls_name:
        boxes_dict[name] = []
    #每个名字对应一个空列表。

    with open(file_path, 'r', encoding='utf-8') as f: #读文件名
        ret_dic = json.load(f)
    # if image_path=="":
    act_h = ret_dic["imageHeight"]
    act_w = ret_dic["imageWidth"]
    # else:
    #     image = cv2.imread(image_path)
    #     act_h, act_w = image.shape[0], image.shape[1]
    annos["imgHeight"] = int(act_h)
    annos["imgWidth"] = int(act_w)
    annos["imageName"] = ret_dic["imagePath"]
    #遍历每个point
    for iter in ret_dic["shapes"]: 
        remove_idx = None
        cls = iter["label"]
        label_info = {}
        if len(iter["points"]) < 2:
            continue
        try:
            [xmin, ymin], [xmax, ymax] = iter["points"] #左下 右上
        except:
            logger.info('返回points 有问题')
            pass
        b = [int(float(xmin)), int(float(ymin)), int(float(xmax)),
                int(float(ymax))]
        if (b[3] - b[1] <= 0) or (b[2] - b[0] <= 0) or (b[3]>act_h) or(b[2]>act_w):
            print("error rect:", b)
            continue

        label_info["location"] = b
        if cls in cls_name: # if in names 
            if remove_idx is not None:
                for ibboxes in boxes_dict[cls]:
                    if remove_element == ibboxes["location"]:
                        boxes_dict[cls].remove(ibboxes)
                        break
            boxes_dict[cls].append(label_info)

        else: #not in name skip it
            continue
    for name in cls_name:
        annos[name] = boxes_dict[name]
    
    return annos

if __name__ == '__main__':
    # root = r'D:\sa_1118'
    # 1.split gold_data
    root = r'D:\sa_data\sa_coco_1'
    save_dir =  r'D:\sa_split_30'  

    test_folder_list = os.listdir(root)
    # test_folder_list = ['norHW_dir']

    bigHW_dirs = os.sep.join([save_dir,'bigger20_dir'])
    norHW_dirs =  os.sep.join([save_dir,'smaller10_dir'])
    midHW_dirs =  os.sep.join([save_dir,'smaller20_dir'])

    for test_folder in test_folder_list:
        bigHW_dir = os.sep.join([bigHW_dirs,'labelme_json'])
        midHW_dir = os.sep.join([midHW_dirs,'labelme_json'])
        norHW_dir = os.sep.join([norHW_dirs,'labelme_json'])#gold_data
        ensure_dir(bigHW_dir)
        ensure_dir(midHW_dir)
        ensure_dir(norHW_dir)
        from01 = glob.glob(f'{root}/{test_folder}/labelme_json/*')
        print(test_folder)
        for json_file_path in from01:
            # split_by_HWr(json_file_path,bigHW_dir,norHW_dir,ratio=10)# 以20为分界线
            split_by_HWr_3(json_file_path,bigHW_dir,norHW_dir,midHW_dir,ratio=20)# 以20为分界线
 