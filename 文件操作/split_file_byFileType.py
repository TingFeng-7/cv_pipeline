# -*- coding: utf-8 -*-
"""
copy 目录

"""
 
import os
import shutil
from loguru import logger
 

source_paths=[]
target_paths = [r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\labelme\imgs'] # 需要检索的一级路径
type_list=['.json','.png']
new_dirs=['jsons','pngs']
dirNames = ['grabbing_open_evaluation'] # 指定目录名
 
 
def copyDir(sourcePath):
    items = os.listdir(sourcePath)
    for item in items:
        filePath = os.path.join(sourcePath, item)
        if os.path.isfile(filePath): # 如果是文件 跳过
                continue
        elif os.path.isdir(filePath):
            # 是目录进一步判断名字是否符合
            if item in dirNames:   
                #递归copy目录
                target_dir = os.path.join(source_paths[0], item)
                shutil.copytree(filePath, target_dir) # delete
                logger.info('复制成功: ' + filePath+'-->'+ target_dir)
            else:
                copyDir(filePath)
        else:
            print('不是目标文件或文件夹 ' + filePath)
 
if __name__ == '__main__':
    for path in target_paths:
        # sourcePath = path
        copyDir(path)