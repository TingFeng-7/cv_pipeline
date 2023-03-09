from sympy import N
from utils.utils1 import read_json_instance,save_json_instance
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



def remove_by_HWr(json_file_path, class_name, save_comps_dir, ratio=8):
    instancefrom = read_json_instance(json_file_path)
    json_name = os.path.basename(json_file_path)
    save_comps_dir_json_to_path = os.sep.join([save_comps_dir, json_name])

    for cls in class_name:
        cur_cls_anno = instancefrom[cls]
        new_cls_anno = []
        for shape in cur_cls_anno:
            p = shape['location']
            try:
                w = abs(p[2]-p[0])+1e-6
                h = abs(p[3]-p[1])+1e-6
                r = max(h/w, w/h)
                if r>= ratio:#宽高比大于20的话
                    continue
                else:
                    new_cls_anno.append(shape) # 原来的插入
            except:
                pass
        instancefrom[cls] = new_cls_anno
    save_json_instance(save_comps_dir_json_to_path, instancefrom)

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
    root = r'D:\sa_data\0010_v1.5_filtered_linebox_yolox'
    save_dir =  r'D:\sa_split_30'  

    test_folder_list = os.listdir(root)
    test_folder_list = ['labelme']
    # test_folder_list = ['save_comps_dir']
    save_comps_dir = os.path.join(root,'sa2comps_smaller8')
    os.makedirs(save_comps_dir, exist_ok=True)
    from tqdm import tqdm
    class_name = ['icon','text', 'image','linebox']
    for test_folder in test_folder_list:
        from01 = glob.glob(f'{root}/{test_folder}/annotations/*')
        print(test_folder)
        for json_file_path in tqdm(from01):
            # split_by_HWr(json_file_path,bigHW_dir,save_comps_dir,ratio=10)# 以20为分界线
            remove_by_HWr(json_file_path, class_name, save_comps_dir,ratio=8)# 以20为分界线
 