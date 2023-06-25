import cv2
import argparse
import json
import os
import numpy as np
from tqdm import tqdm
from colors import _COLORS

# ground-truth xywh
def gt_select_xywh(args):
    # image_path = os.path.join(args.root, args.image_path)
    json_path = os.path.join(args.root, args.gt_json_path)
    json_file = open(json_path)
    infos = json.load(json_file)
    # import pdb;pdb.set_trace()
    outDir = os.path.join(args.root, args.outpath)
    # os.makedirs(outDir, exist_ok=True)
    if not os.path.exists(outDir):
        os.mkdir(outDir)
        
    images = infos["images"]
    annos = infos["annotations"]
    category_id_to_name = infos["categories"]
    font = cv2.FONT_HERSHEY_SIMPLEX
    assert len(images) == len(images)
    # step = 0 
    start =0
    # for i in tqdm(range(len(images))):
    for i in range(len(images)):
        im_id = images[i]["id"]
        im_path = os.path.join(args.root, images[i]["file_name"])
        img = cv2.imread(im_path)
        # print(im_id)
        # for j in annos[start:]:
        step = 0 
        for j in annos[start:]:
            if j["image_id"] == im_id:
                category_id = j["category_id"]
                color = (_COLORS[category_id] * 255).astype(np.uint8).tolist()
                text = '{}'.format(category_id_to_name[category_id]['name']) #输出类名即可
                txt_color = (0, 0, 0) if np.mean(_COLORS[category_id]) > 0.5 else (255, 255, 255)
                txt_bk_color = (_COLORS[category_id] * 255 * 0.7).astype(np.uint8).tolist()
                txt_size = cv2.getTextSize(text, font, 0.4, 1)[0]
                x, y, w, h = j["bbox"]
                x, y, w, h = int(x), int(y), int(w), int(h)
                x2, y2 = x + w, y + h
                img = cv2.rectangle(img, (x, y), (x2, y2), color, thickness=2)
                img = cv2.rectangle(img,(x, y + 1),\
                                    (x + txt_size[0] + 1, y + int(1.5*txt_size[1])),
                                    txt_bk_color, -1)   
                img = cv2.putText(img, text, (x, y + txt_size[1]),\
                                   font, 0.5, txt_color, thickness=1)
                
                img_name = os.path.join(args.root, args.outpath, images[i]["file_name"].split('/')[-1])
                # import pdb;pdb.set_trace()
                step+=1
            else:
                print(f'{im_id} have {step} gt')
                break
                # continue
        cv2.imwrite(img_name, img)
        start += step #记录走过的部署

# ground-truth xyxy
# def gt_select_xyxy(args):
#     json_file = open(args.gt_json_path)
#     infos = json.load(json_file)
#     outDir = os.path.join(args.root, args.outpath)
#     # os.makedirs(outDir, exist_ok=True)

#     if not os.path.exists(outDir):
#         os.mkdir(outDir)

#     images = infos["images"]
#     annos = infos["annotations"]
#     assert len(images) == len(images)
#     for i in tqdm(range(len(images))):
#         im_id = images[i]["id"]
#         im_path = os.path.join(args.image_path, images[i]["file_name"])
#         img = cv2.imread(im_path)
#         for j in range(len(annos)):
#             category_id = j["category_id"]
#             if j["image_id"] == im_id:
#                 x1, y1, x2, y2 = j["bbox"]
#                 x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#                 # object_name = j[""]
#                 img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), thickness=2)  # yellow
#                 img = cv2.putText(img, "{}".format(category_id),(x1 + 5, y1 + 5), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,127,0), 2)
#                 img_name = os.path.join(outDir, images[i]["file_name"].split('/')[-1])
#                 # import pdb;pdb.set_trace()
#                 cv2.imwrite(img_name, img)
#                 # continue
#         # print(i)

category_name = {0: 'person', 1:'child'}
# predict
def predict_select(args):
    infos = json.load(open(args.pred_json_path))
    pred_gt_file = json.load(open(args.gt_json_path))
    image_name_id_map = {i['id']: i['file_name'] for i in pred_gt_file['images']}
    # import pdb;pdb.set_trace()
    for i in tqdm(infos):
        im_path = os.path.join(args.image_path, image_name_id_map[i["image_id"]])
        img_name = os.path.join(args.outpath, image_name_id_map[i["image_id"]])
        score = str(i["score"])
        category = i['category_id']
        if not os.path.exists(img_name):
            img = cv2.imread(im_path)
        else: 
            img = cv2.imread(img_name)
        x, y, w, h = i["bbox"]
        x, y, w, h = int(x), int(y), int(w), int(h)
        x2, y2 = x + w, y + h
        if float(score) >= 0.25:
            cv2.rectangle(img, (x, y), (x2, y2), (0, 0, 255), thickness=2) # red
            cv2.putText(img, "{} {}".format(score, category),(x2, y2 + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,127,0), 2)
        # else:
        #     cv2.rectangle(img, (x, y), (x2, y2), (255, 255, 0), 2)  # green
        img_name = os.path.join(args.outpath, image_name_id_map[i["image_id"]])
        cv2.imwrite(img_name, img)
    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start convert.')
    parser.add_argument('--pred_json_path', type=str, help='predition json file path')
    parser.add_argument('-g','--gt_json_path', type=str, default='',help='predition json file path')
    parser.add_argument('--root', type=str, help='raw image data dir')
    parser.add_argument('--image_path', type=str, help='raw image data dir')
    parser.add_argument('-o','--outpath', type=str, help='image box dir')
    args = parser.parse_args()
    # predict_select(args) # predict json draw box
    gt_select_xywh(args) # gt json draw box (xywh)
    # gt_select_xyxy(args) # gt json draw box (xyxy)
# python  draw_box_coco_json.py --root D:\data\visDrone20191\visdrone2019-yolo --image_path images -g val.json -o ./out