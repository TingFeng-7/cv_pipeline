import os
import os.path as osp
import sys
import cv2
import albumentations as A
import albumentations.augmentations.geometric.resize as are
import numpy as np
import math

def preproc(img, input_size, swap=(2, 0, 1)): 
    if len(img.shape) == 3:
        padded_img = np.ones((input_size[0], input_size[1], 3), dtype=np.uint8) * 114
    else:
        padded_img = np.ones(input_size, dtype=np.uint8) * 114

    r = min(input_size[0] / img.shape[0], input_size[1] / img.shape[1])
    resized_img = cv2.resize(
        img,
        (int(img.shape[1] * r), int(img.shape[0] * r)),
        interpolation=cv2.INTER_LINEAR,
    ).astype(np.uint8)
    padded_img[: int(img.shape[0] * r), : int(img.shape[1] * r)] = resized_img

    padded_img = padded_img.transpose(swap)
    padded_img = np.ascontiguousarray(padded_img, dtype=np.float32)
    return padded_img, r
    
def preproc_32scaled(img, input_size, swap=(2, 0, 1)):

        ori_w,ori_h = img.shape[1],img.shape[0]
        dst_w = max(32,min(input_size[1],math.ceil(img.shape[1]/32)*32))
        dst_h = max(32,min(input_size[0],math.ceil(img.shape[0]/32)*32))
        ratio_w = img.shape[1]/dst_w
        ratio_h = img.shape[0]/dst_h
        new_h = 0
        new_w = 0 
        if ratio_w > 1 or ratio_h > 1:
            # exit()
            if ratio_w > ratio_h:
                new_w = int(img.shape[1]/ratio_w)
                new_h = int(img.shape[0]/ratio_w)
            else:
                new_w = int(img.shape[1]/ratio_h)
                new_h = int(img.shape[0]/ratio_h)
            img = cv2.resize(img, (new_w,new_h),interpolation=cv2.INTER_LINEAR)
            img = cv2.copyMakeBorder(img, 0, input_size[0]-new_h, 0, input_size[1]-new_w, cv2.BORDER_CONSTANT, value=0).astype(np.uint8) #dyn
        else:
            new_w = img.shape[1]
            new_h = img.shape[0]
            img = cv2.copyMakeBorder(img, 0, input_size[0]-new_h, 0, input_size[1]-new_w, cv2.BORDER_CONSTANT, value=0).astype(np.uint8) #dyn
        
        ratio_w = new_w/ori_w
        ratio_h = new_h/ori_h
        # print("*"*100)
        # print(f'ori img shape: {ori_h} and {ori_w}')
        # print(f"new img size:{img.shape}")
        # print("*"*100)

        padded_img = img.transpose(swap)
        padded_img = np.ascontiguousarray(padded_img, dtype=np.float32)
        return padded_img, ratio_w ,ratio_h

        # polys = polys.astype(float)
        # polys[:,0::2] = np.round(polys[:,0::2]*w_scaled_ratio) #改变标注框w的值
        # polys[:,1::2] = np.round(polys[:,1::2]*h_scaled_ratio) #改变标注框h的值
        # polys = polys.astype(int)




def read_path(file_pathname, save_dir):
    #遍历该目录下的所有图片文件
    save_dir_ori = save_dir+'_ori'
    save_dir_new =save_dir+"_new"
    os.makedirs(save_dir_ori, exist_ok=True)
    os.makedirs(save_dir_new, exist_ok=True)
    img_list = get_image_list(file_pathname)
    for filename in img_list:
        #print(filename)
        img = cv2.imread(file_pathname+'/'+filename)
        # new_image = cv2.resize(img, (1366, 768), interpolation=cv2.INTER_AREA) #缩小
        # new_image = cv2.pyrDown(img, (1280,720))
        size = (1280,1280)
        mode = (0,1,2)
        new_image1,r = preproc(img,size, swap=mode)
        new_image2,w_r,h_r = preproc_32scaled(img,size, swap=mode)

        #####保存图片的路径
        cv2.imwrite(osp.join(save_dir_ori,filename), new_image1)
        cv2.imwrite(osp.join(save_dir_new,filename), new_image2)
    print('end')

def get_image_list(file_pathname):
    img_list = [x for x in os.listdir(file_pathname) if x.endswith('png')]
    return img_list


if __name__ == '__main__':

    img_path = r'C:\Users\tingfeng-wu\Desktop\02_github\py_script\image_preprocessing'
    # gt_path = r'D:\sa_data\0011_v1.6_filtered_linebox_yolox\labelme'
    save_dir = './labelme640'

    read_path(img_path, save_dir)