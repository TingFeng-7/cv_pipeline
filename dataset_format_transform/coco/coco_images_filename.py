import json
import os.path as osp
import sys
sys.path.append(r'E:\A01_cyclone\02_github\py_script')
from  utils.utils import *

data_dir =r'E:\visDrone2019'
from tqdm import tqdm

coco_json = osp.join(data_dir, 'VisDrone2019-DET_train_coco.json')

ins = read_json_instance(coco_json)

l = ins['images']


