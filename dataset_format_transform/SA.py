import os

class_name =['icon','text','image','linebox']
def save_result_SAjson_withFineCate(curr_image_bbox_class, curr_image_bboxes, shape, name, class_name,save_folder):
    import json
    result_json={}
    #---
    result_json['imageName'] = name
    result_json['imgHeight'] = shape[0]
    result_json['imgWidth'] = shape[1]
    #--
    for name in class_name:
        result_json[name] = []

    # add
    for i in range(len(curr_image_bboxes)):
        label = curr_image_bbox_class[i]
        if label in class_name:
            result_json[label].append({
                "location":curr_image_bboxes[i],
                "content":"",
                "fine_category": ""
            })
    ##写入json
    os.makedirs(save_folder, exist_ok=True)#确定存在
    name = name[:-4] + '.json'
    json_name = os.path.join(save_folder, name)
    with open(json_name,'w', encoding='utf-8') as fw: 
        json.dump(result_json, fw, indent=2)
        logger.info('{} saved'.format(json_name))