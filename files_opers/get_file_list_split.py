import os
from os.path import join as pathj
path = r'C:\Users\tinfengwu\Downloads'

valpath = pathj(path, 'val')
trainpath = pathj(path, 'train')

split = {'train':[],'val':[]}

with open('low.txt','r') as f:
    for line in f.readlines():
        line = line.split('/')
        split[line[-2]].append(line[-1].split('\n')[0])

if not os.path.exists('./train'):
    os.mkdir('./train')
if not os.path.exists('./val'):
    os.mkdir('./val')


import shutil
for item in split['val']:
    print(item)
    shutil.copyfile(pathj(trainpath, item), pathj('val', item))

for item in split['train']:
    shutil.copyfile(pathj(trainpath, item), pathj('train', item))

