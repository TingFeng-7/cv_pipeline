import os
import cv2
from PIL import Image
from tqdm import tqdm
import json
import datetime

train_type = 'train'
val_type = 'val'
test_type = 'test'

# 待查表
categories = [
    {"id": 0, "name": "ignored regions"},
    {"id": 1, "name": "pedestrian"},
    {"id": 2, "name": "people"},
    {"id": 3, "name": "bicycle"},
    {"id": 4, "name": "car"},
    {"id": 5, "name": "van"},
    {"id": 6, "name": "truck"},
    {"id": 7, "name": "tricycle"},
    {"id": 8, "name": "awning-tricycle"},
    {"id": 9, "name": "bus"},
    {"id": 10, "name": "motor"},
    {"id": 11, "name": "others"}
]

def convert_to_cocodetection_test(dir, output_dir, exist_test=False):
    #数据目录
    train_dir = os.path.join(dir, "test")
    val_dir = os.path.join(dir, "VisDrone2019-DET-val")
    #数据标注目录
    train_annotations = os.path.join(train_dir, "annotations")
    val_annotations = os.path.join(val_dir, "annotations")
    #数据影像目录
    train_images = os.path.join(train_dir, "images")
    val_images = os.path.join(val_dir, "images")
    categories = [
        {"id": 0, "name": "ignored regions"},
        {"id": 1, "name": "pedestrian"},
        {"id": 2, "name": "people"},
        {"id": 3, "name": "bicycle"},
        {"id": 4, "name": "car"},
        {"id": 5, "name": "van"},
        {"id": 6, "name": "truck"},
        {"id": 7, "name": "tricycle"},
        {"id": 8, "name": "awning-tricycle"},
        {"id": 9, "name": "bus"},
        {"id": 10, "name": "motor"},
        {"id": 11, "name": "others"}
    ]
    mode_list = ["test"]
    ## start
    class_name=[]
    for x in categories:
        if x['name'] not in ['others','ignored regions']:
            class_name.append(x['name'])
    categories_new = [ {'id':k, 'name':v} for k,v in enumerate(class_name)]
    ## end
    anno_id_num = 0
    img_id_num = 0
    for mode in mode_list:
        images = []
        annotations = []
        print(f"start loading {mode} data...")
        # anno_id_num -= 1
        # img_id_num -= 1
        if mode == "test":
            set = os.listdir(train_annotations)
            annotations_path = train_annotations
            images_path = train_images
        else:
            set = os.listdir(val_annotations)
            annotations_path = val_annotations
            images_path = val_images
        
        for i in tqdm(set):
            f = open(annotations_path + "/" + i, "r")
            name = i.replace(".txt", "")
            
            #images属性
            image = {}
            image_file_path=images_path + os.sep + name + ".jpg"
            print(image_file_path)

            img_size = Image.open((images_path + os.sep + name+ ".jpg")).size
            width,height=img_size
            # height, width = cv2.imread(images_path + os.sep + name + ".jpg").shape[:2]
            file_name = name + ".jpg"
            image["id"] = img_id_num
            image["height"] = height
            image["width"] = width
            image["file_name"] = file_name
            images.append(image)
            for line in f.readlines():
                #annotation属性
                annotation = {}
                line = line.replace("\n", "")
                if line.endswith(","):  # filter data
                    line = line.rstrip(",")
                line_list = [int(i) for i in line.split(",")]
                if int(line_list[5]) not in [0,11]: # 0和 11 不要
                    bbox_xywh = [line_list[0], line_list[1], line_list[2], line_list[3]]
                    annotation["id"] = anno_id_num
                    annotation["image_id"] = img_id_num
                    # 
                    annotation["category_id"] = int(line_list[5]) - 1
                    # annotation["segmentation"] = []
                    annotation["area"] = bbox_xywh[2] * bbox_xywh[3]
                    # annotation["score"] = line_list[4]
                    annotation["bbox"] = bbox_xywh
                    annotation["iscrowd"] = 0
                    anno_id_num += 1
                    annotations.append(annotation)
            img_id_num += 1

        dataset_dict = {}
        now =datetime.datetime.now()
        dataset_dict['licenses'] =[dict(url=None, id=0, name=None,)]
        dataset_dict['info'] =dict(
            description=None,
            url=None,
            version=None,
            year=now.year,
            contributor=None,
            date_created=now.strftime("%Y-%m-%d %H:%M:%S.%f"))
        dataset_dict["images"] = images
        dataset_dict["annotations"] = annotations
        dataset_dict["categories"] = categories_new
        # json_str = json.dumps(dataset_dict)
        new_json_name =f'{output_dir}/VisDrone2019-DET_{mode}_coco.json'
        save_json(new_json_name, dataset_dict)
        # with open(f'{output_dir}/VisDrone2019-DET_{mode}_coco.json', 'w') as json_file:
        #     json_file.write(json_str)
    print("json file write done...")

def convert_to_cocodetection(dir, output_dir, exist_test=False):
    #数据目录
    train_dir = os.path.join(dir, "train")
    val_dir = os.path.join(dir, "val")
    #数据标注目录
    train_annotations = os.path.join(train_dir, "annotations")
    val_annotations = os.path.join(val_dir, "annotations")
    #数据影像目录
    train_images = os.path.join(train_dir, "images")
    val_images = os.path.join(val_dir, "images")


    mode_list = ["train", "val"]
        ## start
    class_name=[]
    for x in categories:
        if x['name'] not in ['others','ignored regions']:
            class_name.append(x['name'])
    categories_new = [{'id':k, 'name':v} for k,v in enumerate(class_name)]
    merge_class={'ped-people':['people','pedestrian'],
                 'cycle-3':['bicycle', 'tricycle', 'awning-tricycle']}
    i = 0
    for k,v in enumerate(class_name):
        if
    ## end
    anno_id_num = 0
    img_id_num = 0

    for mode in mode_list:
        images = []
        annotations = []

        print(f"start loading {mode} data...")
        if mode == "train":
            set = os.listdir(train_annotations)
            annotations_path = train_annotations
            images_path = train_images
        else:
            set = os.listdir(val_annotations)
            annotations_path = val_annotations
            images_path = val_images
        # anno_id_num -= 1
        # img_id_num -= 1
        for i in tqdm(set):
            f = open(annotations_path + "/" + i, "r")
            name = i.replace(".txt", "")
            #images属性
            image = {}
            image_file_path=images_path + os.sep + name + ".jpg"
            print(image_file_path)

            img_size = Image.open((images_path + os.sep + name+ ".jpg")).size
            width,height=img_size
            # height, width = cv2.imread(images_path + os.sep + name + ".jpg").shape[:2]

            file_name = name + ".jpg"
            image["id"] = img_id_num
            image["height"] = height
            image["width"] = width
            image["file_name"] = file_name
            images.append(image)
            
            for line in f.readlines():
                #annotation属性
                annotation = {}
                line = line.replace("\n", "")
                if line.endswith(","):  # filter data
                    line = line.rstrip(",")
                line_list = [int(i) for i in line.split(",")]
                if int(line_list[5]) not in [0,11]: # 0 和 11 不要
                    bbox_xywh = [line_list[0], line_list[1], line_list[2], line_list[3]]
                    annotation["id"] = anno_id_num
                    annotation["image_id"] = img_id_num
                    annotation["category_id"] = int(line_list[5]) - 1
                    # annotation["segmentation"] = []
                    annotation["area"] = bbox_xywh[2] * bbox_xywh[3]
                    # annotation["score"] = line_list[4]
                    annotation["bbox"] = bbox_xywh
                    annotation["iscrowd"] = 0
                    anno_id_num += 1
                    annotations.append(annotation)
            img_id_num+=1
        dataset_dict = {}
        now =datetime.datetime.now()
        dataset_dict['licenses'] =[dict(url=None, id=0, name=None,)]
        dataset_dict['info'] =dict(
            description=None,
            url=None,
            version=None,
            year=now.year,
            contributor=None,
            date_created=now.strftime("%Y-%m-%d %H:%M:%S.%f"))
        dataset_dict["images"] = images
        dataset_dict["annotations"] = annotations
        dataset_dict["categories"] = categories_new
        # json_str = json.dumps(dataset_dict)
        new_json_name =f'{output_dir}/VisDrone2019-DET_{mode}_coco.json'
        save_json(new_json_name, dataset_dict)
        # with open(f'{output_dir}/VisDrone2019-DET_{mode}_coco.json', 'w') as json_file:
        #     json_file.write(json_str)
    print("json file write done...")
 
def save_json(new_name, json_ins):
    with open(new_name, 'w',encoding='utf-8') as f:
        json.dump(json_ins, f, ensure_ascii=False) #zw
        print('{} saved'.format(new_name)) 
 
def get_test_namelist(dir, out_dir):
    full_path = out_dir + "/" + "test.txt"
    file = open(full_path, 'w')
    for name in tqdm(os.listdir(dir)):
        name = name.replace(".txt", "")
        file.write(name + "\n")
    file.close()
    return None
 
 
def centerxywh_to_xyxy(boxes):
    """
    args:
        boxes:list of center_x,center_y,width,height,
    return:
        boxes:list of x,y,x,y,cooresponding to top left and bottom right
    """
    x_top_left = boxes[0] - boxes[2] / 2
    y_top_left = boxes[1] - boxes[3] / 2
    x_bottom_right = boxes[0] + boxes[2] / 2
    y_bottom_right = boxes[1] + boxes[3] / 2
    return [x_top_left, y_top_left, x_bottom_right, y_bottom_right]
 
 
def centerxywh_to_topleftxywh(boxes):
    """
    args:
        boxes:list of center_x,center_y,width,height,
    return:
        boxes:list of x,y,x,y,cooresponding to top left and bottom right
    """
    x_top_left = boxes[0] - boxes[2] / 2
    y_top_left = boxes[1] - boxes[3] / 2
    width = boxes[2]
    height = boxes[3]
    return [x_top_left, y_top_left, width, height]
 
 
def clamp(coord, width, height):
    if coord[0] < 0:
        coord[0] = 0
    if coord[1] < 0:
        coord[1] = 0
    if coord[2] > width:
        coord[2] = width
    if coord[3] > height:
        coord[3] = height
    return coord
 
 
if __name__ == '__main__':
    # 第一个参数输入上面目录的路径，第二个参数是要输出的路径
    # 只添加了检测训练必要的数据，COCO格式多余的数据都设为空
    dir = r'E:\visDrone20191\visDrone2019_coco'
    convert_to_cocodetection_test(dir,dir)
    convert_to_cocodetection(dir,dir)