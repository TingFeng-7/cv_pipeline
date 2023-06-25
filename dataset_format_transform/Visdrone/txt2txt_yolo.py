import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm

def convert_box(size, box):
    #Convert VisDrone box to YOLO CxCywh box,坐标进行了归一化
    dw = 1. / size[0]
    dh = 1. / size[1]
    return (box[0] + box[2] / 2) * dw, (box[1] + box[3] / 2) * dh, box[2] * dw, box[3] * dh

def xywh2cxcy(img_size, box):
    x1,y1,x2,y2 = int(box[0]),int(box[1]),int(box[2]),int(box[3])
    if x1 < 0:
        x1 = 0.0
        print("\033[0;33;33m", "越界检查,x1小于0,错误数据:", x1, "已修订为:", "\033[0m")

    elif x1 > img_size[0]:
        x1 = float(img_size[0])
        print("\033[0;33;33m", "越界检查,x1大于宽,错误数据:", x1, "已修订为:", "\033[0m")

    if y1 < 0:
        y1 = 0.0
        print("\033[0;33;33m", "越界检查,y1小于0,错误数据:", y1, "已修订为:","\033[0m")

    elif y1 > img_size[1]:
        y1 = float(img_size[1])
        print("\033[0;33;33m", "越界检查,y1大于高,错误数据:", y1, "已修订为:","\033[0m")

    if x2 < 0:
        x2 = 0.0
        print("\033[0;33;33m", "越界检查,x2小于0,错误数据:", x2, "已修订为:", "\033[0m")

    elif x2 > img_size[0]:
        x2 = float(img_size[0])
        print("\033[0;33;33m", "越界检查,x2大于宽,错误数据:", x2, "已修订为:",  "\033[0m")

    if y2 < 0:
        y2 = 0.0
        print("\033[0;33;33m", "越界检查,y2小于0,错误数据:", y2, "已修订为:","\033[0m")

    elif y2 > img_size[1]:
        y2 = float(img_size[1])
        print("\033[0;33;33m", "越界检查,y2大于高,错误数据:", y2, "已修订为:", "\033[0m")
    # 2.转换并归一化 robust
    center_x = (x1 + x2) * 0.5 / img_size[0]
    center_y = (y1 + y2) * 0.5 / img_size[1]
    w = abs((x2 - x1)) * 1.0 / img_size[0]
    h = abs((y2 - y1)) * 1.0 / img_size[1]
    return center_x, center_y, w, h

def visdrone2yolo(dir):

    # (dir / 'labels').mkdir(parents=True, exist_ok=True)  # make labels directory
    (dir / 'Annotations_YOLO').mkdir(parents=True, exist_ok=True)  # make labels directory
    pbar = tqdm((dir / 'annotations').glob('*.txt'), desc=f'Converting {dir}')
    for f in pbar:
        img_size = Image.open((dir / 'images' / f.name).with_suffix('.jpg')).size
        lines = []
        with open(f, 'r') as file:  # read annotation.txt
            for row in [x.split(',') for x in file.read().strip().splitlines()]:
                if row[4] == '0':  # VisDrone 'ignored regions' class 0
                    continue
                cls = int(row[5]) - 1
                box = convert_box(img_size, tuple(map(int, row[:4])))
                lines.append(f"{cls} {' '.join(f'{x:.6f}' for x in box)}\n")
                with open(str(f).replace(os.sep + 'annotations' + os.sep, os.sep + 'labels_YOLO' + os.sep), 'w') as fl:
                    fl.writelines(lines)  # write label.txt

def visdrone2yolo_my(dir, d):

    # (dir / 'labels').mkdir(parents=True, exist_ok=True)  # make labels directory
    (dir / 'labels'/ d ).mkdir(parents=True, exist_ok=True)  # make labels directory
    pbar = tqdm((dir / d/ 'annotations').glob('*.txt'), desc=f'Converting {dir}')
    for f in pbar:
        img_size = Image.open((dir / d /'images' / f.name).with_suffix('.jpg')).size
        lines = []
        with open(f, 'r') as file:  # read annotation.txt
            for row in [x.split(',') for x in file.read().strip().splitlines()]:
                if row[4] == '0':  # VisDrone 'ignored regions' class 0
                    continue
                cls = int(row[5]) - 1
                box = convert_box(img_size, tuple(map(int, row[:4])))
                lines.append(f"{cls} {' '.join(f'{x:.6f}' for x in box)}\n")
                txtname = os.path.basename(str(f))
                with open(str((dir/'labels'/ d /txtname)), 'w') as fl:
                    fl.writelines(lines)  # write label.txt

dir = Path(r'E:\VisDrone2019')  # dataset文件夹下Visdrone2019文件夹路径
# Convert
for d in 'VisDrone2019-DET-train', 'VisDrone2019-DET-val', 'VisDrone2019-DET-test-dev':
    # visdrone2yolo(dir / d)  # convert VisDrone annotations to YOLO labels
    visdrone2yolo_my(dir, d)
