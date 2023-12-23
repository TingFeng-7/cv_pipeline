import json
from os.path import join as pathj
import os
import numpy as np

def iou(a, b):
    # 计算两个检测框之间的iou
    w_a = a[2] - a[0]
    h_a = a[3] - a[1]
    w_b = b[2] - b[0]
    h_b = b[3] - b[1]

    area_a = w_a * h_a
    area_b = w_b * h_b

    w = min(b[2], a[2]) - max(b[0], a[0])
    h = min(b[3], a[3]) - max(b[1], a[1])

    if w <= 0 or h <= 0:
        return 0

    area_c = w * h

    return area_c / (area_a + area_b - area_c)

def get_iou_thresh(a):
    # 文本采用动态iou，最大可以到MAX_IOU，对于小目标最小iou可以到0.1。
    w_a = a[2] - a[0]
    h_a = a[3] - a[1]
    area = (w_a + 1) * (h_a + 1)
    iou_thresh = min((area+50)/500, 0.5)
    return iou_thresh
    
def read_json(abs_txt_name):
    with open(abs_txt_name, 'r', encoding='utf-8') as f: #读文件名
        ret_dic = json.load(f)
        return ret_dic
        
def save_json(new_name,json_ins):
    with open(new_name, 'w',encoding='utf-8') as f:
        json.dump(json_ins ,f ,indent=2,ensure_ascii=False)#zw
        print('{} saved'.format(new_name)) 

if __name__ == '__main__':
    dir = 'D:\sa_data\sa_coco_1\labelme\comps_linebox_subcate'
    predicts = r'D:\sa_data\f36_exps\20221124_aware_hardnms_conf10_iou50\Element_grabbing\grabbing_evaluation\labelme\grabbing_predict'
    cls_name_need = ['inputbox', 'v_segline', 'tab', 'track', 
        'linebox', 'h_segline', 'scrollbar_slider']

    tps_dict = {}
    gold_dict= {}
    recall_dict= {}
    pred_dict= {'linebox_predict':0}
    pred_fault_box= {'linebox_fault':[]}
    for name in cls_name_need:
        tps_dict[name+'_tp'] = 0
        gold_dict[name+'_gold'] = 0
        recall_dict[name+'_recall'] = 0

    pred_correct =0 
    for name in os.listdir(dir): #每个文件进行对比
        pred_ins = read_json(pathj(predicts, name))
        gold_ins = read_json(pathj(dir, name))
        print(f'comparing : {name}')
        dt_per_img = []
        gt_per_img = []
        dt = pred_ins['linebox']
        pred_dict['linebox_predict'] += len(dt)
        for e in dt:
            dt_per_img.append({'box':e['location'], 'label': 'linebox'})
        for name in cls_name_need:
            gt = gold_ins[name]
            gold_dict[name+'_gold'] += len(gold_ins[name]) #计算 所有gt
            for g in gt:
                gt_per_img.append({'box':g['location'], 'label':name})

        #一张图的 dt和gt都有了
        predict_status = np.zeros(len(dt_per_img), dtype=np.int)
        for gt in gt_per_img:
            dyn_iou = get_iou_thresh(gt['box'])
            iou_thresh = min(0.5, dyn_iou)
            count = -1
            for dt in dt_per_img:
                count+=1
                if predict_status[count] == 0:
                    cur_iou = iou(gt['box'], dt['box'])
                    cur_gt_label = gt['label']
                    if cur_iou > iou_thresh:
                        tps_dict[cur_gt_label+'_tp']+=1
                        predict_status[count] = 1
                        pred_correct+=1
                        break
                    else:
                        continue
                else: 
                    continue
        fault = [v for k,v in enumerate(dt_per_img) if predict_status[k]==0]#没用过的 框
        if len(fault)!=0:
            for e in fault:
                pred_fault_box['linebox_fault'].append(e)
    # for key.split('_')[0] in gold_dict.keys():
    for key in cls_name_need:
        recall_dict[key+'_recall'] = tps_dict[key+'_tp'] / gold_dict[key+'_gold']
    print(json.dumps(tps_dict, indent=4,sort_keys=True))
    print(json.dumps(gold_dict ,indent=4, sort_keys=True))
    print(json.dumps(recall_dict ,indent=4, sort_keys=True))

    print(json.dumps(pred_dict ,indent=4, sort_keys=True))
    
    print(pred_correct/pred_dict['linebox_predict'])
    save_json("linebox_fault.json",pred_fault_box)