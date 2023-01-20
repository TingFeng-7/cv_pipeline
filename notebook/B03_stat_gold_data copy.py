import json
import os
from os.path import join as pathj
root_dir = r'D:\sa_data\f36_exps\20221124_aware_hardnms_conf10_iou50\Element_grabbing\grabbing_evaluation\labelme\grabbing_evaluation_statistics\statistic_0.5_0.5_0.5_0\detect'
miss = 'button_miss' #有label
fault = 'button_fault'
miss_dir = os.path.join(root_dir,miss)
fault_dir = os.path.join(root_dir,fault)
# 读取json
def read_json(abs_txt_name):
    with open(abs_txt_name, 'r', encoding='utf-8') as f: #读文件名
        ret_dic = json.load(f)
    return ret_dic
        
def save_json(new_name,json_ins):
    with open(new_name, 'w',encoding='utf-8') as f:
        json.dump(json_ins ,f ,indent=2,ensure_ascii=False)#zw
        print('{} saved'.format(new_name)) 

if __name__ == '__main__':
    gold_dir = r'D:\sa_split_32'
    stat_dict ={}
    class_name = [] 
    # cls_map = {'text':['icon_text'],
    #                 'icon':['arrow','mohu'],
    #                 'linebox':['inputbox','scrollbar_slider', 'track', 'h_segline', 'v_segline', 'tab', 'linebox']}

    class_names = ['text','icon','image','linebox'] 
    for sub in os.listdir(gold_dir):
        print(sub)
        json_dir = pathj(gold_dir, sub, 'comps')
        if os.path.isdir(json_dir):
            for filename in os.listdir(json_dir):
                ins = read_json(pathj(json_dir, filename))
                for cls in class_name:
                    stat_dict[sub+'_'+cls+'_gold'] += len(ins[cls])

