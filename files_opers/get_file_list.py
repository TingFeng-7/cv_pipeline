import os

path = r'D:\data\hubmap_imagenet\val'
with open('files.txt','w') as f:
    f.writelines(f + ' 0' + '\n' for f in os.listdir(path))