import json
import cv2
from os.path import join as pathj
from tqdm import tqdm
# 输入和输出json文件路径
root_path = r'D:\data\visDrone20191\visdrone2019-yolo'
input_json_file = pathj(root_path,'train.json')
output_json_file = pathj(root_path,'train_1280.json')


# 目标尺寸
target_size = (1280, 768) #w,h

with open(input_json_file, 'r') as f:
    data = json.load(f)
imgs_info = data['images']
imgid_filename = {i['id']:i['file_name'] for i in imgs_info}

imgid_info = {i['id']:i for i in imgs_info}
visited = [0]*len(imgs_info)



for item in tqdm(data['annotations']):
    # 读取原图
    image_id = item['image_id']
    # img_path = pathj(root_path, imgid_filename[image_id])
    # 获取原图尺寸
    # img = cv2.imread(img_path)
    # h, w = img.shape[:2]
    # if image_id :
    h,w = imgid_info[image_id]['height'],imgid_info[image_id]['width']

    # 计算缩放比例
    scale_x = target_size[0] / w #1280/1920
    scale_y = target_size[1] / h  #768/1080
    scale = min(scale_x, scale_y) #根据两边最长边进行缩放
    scale = round(scale,2)
    # print(f'min({scale_x}, {scale_y}) : {scale}')
    # 缩放bbox坐标

    bbox = item['bbox']
    bbox[0] *= scale
    bbox[1] *= scale
    bbox[2] *= scale
    bbox[3] *= scale
    item['bbox'] = [int(p) for p in bbox]

    # 更新image信息
    if visited[image_id] == 0:
        # imgid_info[image_id]['width'] = target_size[0]
        # imgid_info[image_id]['height'] = target_size[1]
        imgid_info[image_id]['scale'] = scale

# 写回json文件
with open(output_json_file, 'w') as f:
    json.dump(data, f)