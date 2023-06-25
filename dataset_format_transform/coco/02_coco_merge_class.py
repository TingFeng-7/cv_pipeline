import json
from os.path import join as pathj

root_path = r'D:\data\visDrone20191\visdrone2019-yolo'
input_json_file = pathj(root_path,'train.json')
output_json_file = pathj(root_path,'train_7.json')

json_file = input_json_file  # 替换为你的 JSON 文件路径
target_categories = ['pedestrian', 'people']  # 替换为你要合并的类别

with open(json_file, 'r') as f:
    data = json.load(f)

# 将 target_categories 中的所有类别合并成一个新的类别 "pet"
new_category = "ped-people"

# 遍历所有标注信息
for annotation in data['annotations']:
    # 如果当前标注信息的类别在 target_categories 中，则修改为新的类别
    if data['categories'][annotation['category_id']]['name'] in target_categories:
        annotation['category_id'] = data['categories'].index(
            {'supercategory': '', 'id': len(data['categories']), 'name': new_category})
    else:
        continue

# 修改 categories 中的信息，将新的类别添加到列表中
data['categories'].append({'supercategory': '', 'id': len(data['categories']), 'name': new_category})

# 保存结果
with open(output_json_file, 'w') as f:
    json.dump(data, f)