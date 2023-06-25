import argparse
import json
import multiprocessing
import os

import cv2
from pycocotools.coco import COCO

def resize_img(img_path, output_path, size):
    img = cv2.imread(img_path)
    img = cv2.resize(img, size)
    cv2.imwrite(output_path, img)

def process_img(info):
    img_id, img_path, coco, size, output_dir = info
    ann_ids = coco.getAnnIds(imgIds=img_id)
    anns = coco.loadAnns(ann_ids)
    img_name = os.path.basename(img_path)
    img_ext = os.path.splitext(img_name)[1]

    # Resize image
    output_path = os.path.join(output_dir, img_name)
    resize_img(img_path, output_path, size)

    # Update annotation information
    for ann in anns:
        bbox = ann['bbox']
        bbox[0] *= size[0] / coco.imgs[img_id]['width']
        bbox[1] *= size[1] / coco.imgs[img_id]['height']
        bbox[2] *= size[0] / coco.imgs[img_id]['width']
        bbox[3] *= size[1] / coco.imgs[img_id]['height']
        ann['bbox'] = bbox
        ann['area'] = bbox[2] * bbox[3]
        ann['segmentation'] = []

    # Save updated annotations to file
    ann_file_path = os.path.join(output_dir, 'annotations', f"{img_id:012d}.json")
    with open(ann_file_path, 'w') as f:
        json.dump(anns, f)

def process_images(img_dir, output_dir, ann_file, size, num_processes):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'annotations'), exist_ok=True)

    # Load COCO annotations
    coco = COCO(ann_file)

    # Process images in parallel
    img_infos = [(img_id, os.path.join(img_dir, coco.imgs[img_id]['file_name']), coco, size, output_dir) 
                 for img_id in coco.getImgIds()]
    with multiprocessing.Pool(num_processes) as p:
        p.map(process_img, img_infos)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resize COCO dataset')
    parser.add_argument('--img_dir', type=str, required=True, help='path to directory containing images')
    parser.add_argument('--output_dir', type=str, required=True, help='path to output directory')
    parser.add_argument('--ann_file', type=str, required=True, help='path to COCO annotation file')
    parser.add_argument('--size', type=int, nargs=2, required=True, help='output size as (width, height)')
    parser.add_argument('--num_processes', type=int, default=4, help='number of processes to use for resizing')

    args = parser.parse_args()

    process_images(args.img_dir, args.output_dir, args.ann_file, args.size, args.nu