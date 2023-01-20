# -*- coding: utf-8 -*-
"""
copy 目录

"""
 
import os
import shutil
from loguru import logger
 
source_paths=[]
target_paths = \
    [r'D:\sa_copy\exps\2022.9.30_yolox_1080p_sa_f27\Element_grabbing\grabbing_evaluation'] # 需要检索的一级 路径
dirNames = ['grabbing_open_evaluation'] # 指定目录名
 
 
def copyDir(sourcePath):
    items = os.listdir(sourcePath)
    for item in items:
        filePath = os.path.join(sourcePath, item)
        # 如果是文件跳过
        if os.path.isfile(filePath): 
                continue
        elif os.path.isdir(filePath) and item in dirNames:
            # 是目录 且 名字命中
            target_dir = os.path.join(source_paths[0], item)
            shutil.copytree(filePath, target_dir) # delete
            logger.info('复制成功: ' + filePath+ '-->'+ target_dir)
        elif not item in dirNames:
            copyDir(filePath)
        else:
            print('不是目标文件或文件夹 ' + filePath)
 
if __name__ == '__main__':
    for path in target_paths:
        # sourcePath = path
        copyDir(path)