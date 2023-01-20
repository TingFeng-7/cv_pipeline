from common.py_util.util import *
from common.cv.util import *
from common.data.util import check_overlap_boxes


class Labelme_res():
    def __init__(self, label_file=None):
        if label_file is None:
            self.labelme_json = write_labelme_json()
        elif isinstance(label_file, str):
            self.labelme_json = json_load(label_file)
        elif isinstance(label_file, dict):
            self.labelme_json = label_file
        elif isinstance(label_file, list):
            self.labelme_json = self.from_std(label_file)
        else:
            raise Exception("label_file type error")

    def set_info(self, img_path, img):
        h, w = img.shape[:2]
        self.labelme_json["imagePath"] = img_path
        self.labelme_json["imageWidth"] = w
        self.labelme_json["imageHeight"] = h
        return self.labelme_json

    def to_json(self):
        return self.labelme_json

    def get_objects(self):
        return self.labelme_json["shapes"]

    def add_object(self, labelme_object):
        self.labelme_json["shapes"].append(labelme_object)
        return self.labelme_json

    def sort(self):
        self.labelme_json["shapes"].sort(
            key=lambda t: [t["label"], t["points"]])
        return self.labelme_json

    def merge(self, labelme_res2):
        # assert info same
        # for key in ["imageWidth", "imageHeight",]:
        #     if self.labelme_json[key] != labelme_res2.labelme_json[key]:
        #         print(
        #             f"{key} not same: {self.labelme_json[key]}, {labelme_res2.labelme_json[key]}")
        #         return False
        self.labelme_json["shapes"] += labelme_res2.labelme_json["shapes"]
        self.sort()
        return True

    def dump(self, json_path):
        json_dump(json_path, self.labelme_json)
        return True

    def crop_sub(self, output_folder, img_root="", img_path=""):
        if img_path == "":
            img_path = self.labelme_json["imagePath"]
        else:
            img_path = pathj(img_root, img_path)
        img = cv2_imread(img_path)
        std_boxes = self.to_std()
        for i, std_box in enumerate(std_boxes):
            img_crop = crop_box(img, std_box)
            class_i = get_std_box_class(std_box)
            img_save_path = pathj(output_folder, f"{i}.jpg")
            cv2_imwrite(img_save_path, img_crop)
        return True

    def draw(self, img, img_save_path=None):
        img_draw = draw_boxes_std(img, self.to_std())
        if img_save_path is not None:
            cv2_imwrite(img_save_path, img_draw)
        return img_draw

    def to_std(self):
        std_boxes = list(map(self.object2std, self.get_objects()))
        return std_boxes

    def to_sa_v2(self):
        from common.data.sa_api_v2 import write_sa_v2_json
        std_labels = self.to_std()
        sa_v2_json = write_sa_v2_json(std_labels, self.labelme_json["imagePath"],
                                      self.labelme_json["imageHeight"], self.labelme_json["imageWidth"])
        return sa_v2_json

    def to_sa_v1(self):
        sa_v1_json = labelme2sav1(self.labelme_json, self.labelme_json["imagePath"],
                                  self.labelme_json["imageHeight"], self.labelme_json["imageWidth"])
        return sa_v1_json

    def to_sa_v3(self):

        return

    def to_coco(self):

        return

    @staticmethod
    def object2std(ann):
        points = ann["points"]
        score = ann.get("score", 1.0)
        x_list = [p[0] for p in points]
        y_list = [p[1] for p in points]
        x1, y1, x2, y2 = min(x_list), min(y_list), max(x_list), max(y_list)
        bbox_i = [x1, y1, x2, y2]
        bbox_i = list(map(round, bbox_i))
        class_i = ann["label"]
        return [*bbox_i, class_i, score]

    @staticmethod
    def change_box(ann, box):
        ann["points"] = [box[:2], box[2:4]]
        return ann

    @staticmethod
    def from_std(std_boxes, img_name="unknown",
                 image_height="unknown", image_width="unknown"):
        detect_dicts = []
        for box in std_boxes:
            class_i = get_std_box_class(box)
            score_i = get_std_box_score(box)
            if len(box) > 4:
                class_i = box[4]
            detect_dict_i = {"class": class_i,
                             "box": box[:4], "score": score_i}
            detect_dicts.append(detect_dict_i)
        labelme_json = write_labelme_json(
            detect_dicts, img_name, image_height, image_width)
        labelme_sort(labelme_json)

        return Labelme_res(labelme_json)

    @staticmethod
    def check():
        pass


def labelme_check_script(labelme_json_folder, overlap_iou_thresh=1.0):
    '''
    check if boxes in labelme_json_folder too overlap
    '''
    labelme_json_folder_conflict = labelme_json_folder + "_conflict"
    labelme_json_folder_valid = labelme_json_folder + "_valid"
    labelme_count = 0
    labelme_conflict_count = 0
    for labelme_json_name in tqdm.tqdm(os.listdir(labelme_json_folder), desc=f"labelme_check_script on {labelme_json_folder}"):
        if not labelme_json_name.endswith(".json"):
            continue
        labelme_count += 1
        labelme_json_path = pathj(labelme_json_folder, labelme_json_name)
        labelme_json_orig = json_load(labelme_json_path)
        # labelme_json = labelme_json_orig.copy()
        labelme_json = copy.deepcopy(labelme_json_orig)
        if "shapes" not in labelme_json:
            labelme_json = labelimg2labelme(labelme_json)

        '''check w, h'''
        file_key = labelme_json_name.replace(".json", "")
        img_path = pathj(labelme_json_folder.replace(
            "labelme_json", "imgs"), f"{file_key}.png")
        assert os.path.exists(img_path), f"{img_path} not exists"
        img = cv2_imread(img_path)
        h, w = img.shape[:2]
        if labelme_json["imageWidth"] != w:
            print(f"{labelme_json['imageWidth']} != {w}")
            labelme_json_orig["imageWidth"] = w
        if labelme_json["imageHeight"] != h:
            print(f"{labelme_json['imageHeight']} != {h}")
            labelme_json_orig["imageHeight"] = h

        labelme_json_valid, labelme_json_conflict = labelme_json_check(
            labelme_json, overlap_iou_thresh=overlap_iou_thresh, return_conflict=True)

        json_dump(pathj(labelme_json_folder_valid,
                        f"{file_key}.json"), labelme_json_valid)
        copy2(img_path, pathj(
            labelme_json_folder_valid, f"{file_key}.png"))
        if len(labelme_json_conflict["shapes"]) == 0:
            continue

        labelme_conflict_count += 1
        print(f"labelme_todo_percent: {labelme_conflict_count / labelme_count}, \
            labelme_conflict_count: {labelme_conflict_count}, labelme_count: {labelme_count}")
        json_dump(pathj(labelme_json_folder_conflict,
                        f"{file_key}.json"), labelme_json_conflict)
        copy2(img_path, pathj(
            labelme_json_folder_conflict, f"{file_key}.png"))
    status_res = {"labelme_count": labelme_count,
                  "labelme_conflict_count": labelme_conflict_count}
    return status_res

# def labelme_check_script_sa(sa_root):
#     labelme_count = 0
#     labelme_conflict_count = 0
#     software_names = os.listdir(sa_root)
#     for sw_name in tqdm.tqdm(software_names, desc="labelme_check_script on softwares"):
#         sw_folder = pathj(sa_root, sw_name)
#         if not os.path.isdir(sw_folder):
#             continue
#         labelme_json_folder = pathj(sw_folder, "labelme_json")


def get_labelme_box(ann):
    points = ann["points"]
    if len(points) < 2:
        return None
    x_list = [p[0] for p in points]
    y_list = [p[1] for p in points]
    if len(x_list) < 2 or len(y_list) < 2:
        return None
    x1, y1, x2, y2 = min(x_list), min(y_list), max(x_list), max(y_list)
    bbox_i = [x1, y1, x2, y2]
    bbox_i = list(map(round, bbox_i))
    return bbox_i


def labelme_json_check(labelme_json, overlap_iou_thresh=1.0, return_conflict=False):
    '''
    check if boxes are too overlap
    '''
    w, h = labelme_json["imageWidth"], labelme_json["imageHeight"]
    labelme_json_tpl = labelme_json.copy()
    labelme_json_tpl["shapes"] = []
    labelme_json_res = copy.deepcopy(labelme_json_tpl)
    boxes = []
    for i, ann in enumerate(labelme_json["shapes"]):
        bbox_i = get_labelme_box(ann)
        if bbox_i is None:
            continue
        bbox_i = std_box(bbox_i, w, h)
        ann = Labelme_res.change_box(ann, bbox_i)
        if not legal_box(bbox_i, w, h):
            box_std = std_box(bbox_i[:4], w, h)
            print(f"{bbox_i} is illegal, turn to {box_std}")
            bbox_i[:4] = box_std
            if not legal_box(bbox_i, w, h):
                print(f"{box_std} is still illegal, return")
                continue
        boxes.append(bbox_i)
        labelme_json_res["shapes"].append(ann)

    boxes2overlap = check_overlap_boxes(
        boxes, overlap_iou_thresh=overlap_iou_thresh)

    labelme_json_valid = copy.deepcopy(labelme_json_tpl)
    labelme_json_conflict = copy.deepcopy(labelme_json_tpl)
    for i, ann in enumerate(labelme_json_res["shapes"]):
        if boxes2overlap[i] == 0:  # clean
            labelme_json_valid["shapes"].append(ann)
        elif boxes2overlap[i] == 1:  # partial
            labelme_json_conflict["shapes"].append(ann)

    if return_conflict:
        ''' output conflit '''
        return labelme_json_valid, labelme_json_conflict
    else:
        return labelme_json_valid


def labelme_sort(labelme_json):
    # def sort_func(shape_i, shape_j):
    #     if shape_i[""]
    #     return
    # labelme_json["shapes"].sort(key=functools.cmp_to_key(sort_func))

    labelme_json["shapes"].sort(key=lambda t: [t["label"], t["points"]])

    return labelme_json


def labelme_object2std(ann):
    points = ann["points"]
    x_list = [p[0] for p in points]
    y_list = [p[1] for p in points]
    x1, y1, x2, y2 = min(x_list), min(y_list), max(x_list), max(y_list)
    bbox_i = [x1, y1, x2, y2]
    bbox_i = list(map(round, bbox_i))
    class_i = ann["label"]
    return [*bbox_i, class_i, 1.0]


def write_labelme_json(detect_labels=[], imgName="unknown", imageHeight="unknown", imageWidth="unknown"):
    '''
    detect_labels: [detect_label_i...]
        :detect_label_i: {"class":class_i, "box":box_i}
    '''
    data_dict = {"version": "4.5.7", "flags": {}, "shapes": [], "imageData": None,
                 "imagePath": imgName,   "imageHeight": imageHeight, "imageWidth": imageWidth}
    for detect_label_i in detect_labels:
        class_i = detect_label_i["class"]
        score_i = detect_label_i.get("score", 1.0)
        box_i = detect_label_i["box"]

        shape_i = {"label": class_i,
                   "group_id": None,
                   "shape_type": "rectangle",
                   "flags": {},
                   "points": [box_i[:2], box_i[2:]],
                   "score": score_i}

        data_dict["shapes"].append(shape_i)
    return data_dict


def std2labelme(boxes_, img_name, image_height, image_width):
    detect_dicts = []
    for box in boxes_:
        class_i = get_std_box_class(box)
        if isinstance(class_i, list):
            class_i = "_".join(class_i)
        detect_dict_i = {"class": class_i, "box": box[:4]}
        detect_dicts.append(detect_dict_i)
    labelme_json = write_labelme_json(
        detect_dicts, img_name, image_height, image_width)
    labelme_sort(labelme_json)
    return labelme_json


def write_labelme_dict(detect_labels, imgName, imageHeight, imageWidth):
    '''
    detect_labels: [detect_label_i...]
        :detect_label_i: {"class":class_i, "box":box_i}
    '''
    data_dict = {"version": "4.5.7", "flags": {}, "shapes": [], "imageData": None,
                 "imagePath": imgName,   "imageHeight": imageHeight, "imageWidth": imageWidth}
    for detect_label_i in detect_labels:
        class_i = detect_label_i["class"]
        box_i = detect_label_i["box"]

        shape_i = {"label": class_i,
                   "group_id": None,
                   "shape_type": "rectangle",
                   "flags": {},
                   "points": [box_i[:2], box_i[2:]]}

        data_dict["shapes"].append(shape_i)
    return data_dict


def labelme2std(labelme_dict):
    bboxes_ = []
    for i, ann in enumerate(labelme_dict["shapes"]):
        class_i = ann["label"]
        points = ann["points"]
        x_list = [p[0] for p in points]
        y_list = [p[1] for p in points]
        x1, y1, x2, y2 = min(x_list), min(y_list), max(x_list), max(y_list)
        bbox_i = [x1, y1, x2, y2]
        bbox_i = list(map(round, bbox_i))
        bboxes_.append([*bbox_i, class_i])

    return bboxes_


def labelimg2labelme(labelimg_dict):
    labelme_annos = {}
    h = float(labelimg_dict["imgHeight"])
    w = float(labelimg_dict["imgWidth"])
    labelme_annos['imageHeight'] = int(h)
    labelme_annos['imageWidth'] = int(w)
    labelme_annos['imagePath'] = labelimg_dict["image_name"]
    shapes = []
    for iter_i in labelimg_dict["attrbutes"]:
        label = iter_i["label"]
        b = [int(float(iter_i["data"][0]) * w), int(float(iter_i["data"][1] * h)), int(float(iter_i["data"][2]) * w),
             int(float(iter_i["data"][3]) * h)]
        shape = {"label": label, "points": [b[:2], b[2:]],
                 "shape_type": "rectangle", }
        shapes.append(shape)
    labelme_annos['shapes'] = shapes
    return labelme_annos


def labelme2sav1(labelme_dict, imagePath, imageHeight, imageWidth):

    sa_v1_json = {"imageName": imagePath,
                  "imgHeight": imageHeight,
                  "imgWidth": imageWidth,
                  'icon': [],
                  'text': []}
    for dic in labelme_dict['shapes']:
        if dic['label'] == 'icon':
            icon_elem = {'location': np.array(
                dic['points'][0]+dic['points'][1]).tolist()}
            sa_v1_json['icon'].append(icon_elem)
        if dic['label'] == 'text':
            text_elem = {'location': np.array(
                dic['points'][0]+dic['points'][1]).tolist(), "content": ""}
            sa_v1_json['text'].append(text_elem)

    return sa_v1_json


def crop_sub_script_i(labelme_folder, output_folder,
                      software_name="", crop_label=False, box_enlarge_pix=0,):
    '''
    :param :
        crop_label: if True, crop the sub image and crop the label, 
            for simplicity, remain the label that area > 0
    '''
    if labelme_folder.endswith("labelme_json"):
        img_folder = labelme_folder.replace("labelme_json", "imgs")
    else:
        img_folder = labelme_folder
    for labelme_file in tqdm.tqdm(os.listdir(labelme_folder)):
        if not labelme_file.endswith(".json"):
            continue
        file_key = get_file_key(labelme_file)
        labelme_path = os.path.join(labelme_folder, labelme_file)
        labelme_dict = json_load(labelme_path)
        image_path = labelme_path.replace(".json", ".png").replace(
            labelme_folder, img_folder)
        # image = cv2_imread(image_path)
        image = cv2_imread(image_path, flags=cv2.IMREAD_UNCHANGED)
        if len(image.shape) == 3 and image.shape[-1] == 4:
            if image[..., -1].min() == 255:
                # regard as normal rbg
                image = image[..., :-1]
            else:
                # ignore transparent
                continue

        image_height, image_width = image.shape[:2]
        bboxes = labelme2std(labelme_dict)
        image_name = labelme_dict["imagePath"]
        for i, bbox in enumerate(bboxes):
            class_ = get_std_box_class(bbox)

            sub_image_save_path = pathj(
                output_folder, class_, f"{software_name}_{file_key}_{str(bbox)}.png")
            # image_name = f"{class_}_{software_name}_{file_key}_{i}.png"
            # sub_image_save_path = pathj(
            #     output_folder, image_name)
            bbox = std_box(bbox, image_width, image_height)
            if not legal_box(bbox, image_width, image_height):
                continue
            if box_enlarge_pix != 0:
                bbox = enlarge_box(bbox, box_enlarge_pix, image)
            sub_image = crop_box(image, bbox)
            cv2_imwrite(sub_image_save_path, sub_image)
            if crop_label:
                sub_labels = []
                sub_label_save_path = change_ext(sub_image_save_path, ".json")
                h_sub, w_sub = sub_image.shape[:2]
                for bbox_j in bboxes:
                    bbox_j_crop = offset_box(
                        bbox_j, (-bbox[0], -bbox[1]))
                    bbox_j_crop = std_box(bbox_j_crop, w=w_sub, h=h_sub)
                    if get_area(bbox_j_crop) > 0:
                        sub_labels.append(bbox_j_crop)
                Labelme_res.from_std(
                    sub_labels, image_name, *sub_image.shape[:2]).dump(sub_label_save_path)


def crop_sub_script(input_folder, output_folder=None, box_enlarge_pix=0):
    # output_folder = ensure_dir(input_folder + "crop_sub")
    if output_folder is None:
        output_folder = ensure_dir(pathj(input_folder + "_crop_sub", "gather"))
    for software_i in tqdm.tqdm(os.listdir(input_folder), desc="crop_sub_script"):
        software_i_path = os.path.join(
            input_folder, software_i, "labelme_json")
        if not os.path.isdir(software_i_path):
            software_i_path = os.path.join(input_folder, software_i, "imgs")
        if not os.path.isdir(software_i_path):
            continue
        # crop_sub_script_i(software_i_path, output_folder=output_folder_software)
        crop_sub_script_i(
            software_i_path,  output_folder=output_folder,
            software_name=software_i, box_enlarge_pix=box_enlarge_pix,)
    return


def modify_labelme_script_i(labelme_folder, output_folder, map_func):
    '''
    :param :
        crop_label: if True, crop the sub image and crop the label, 
            for simplicity, remain the label that area > 0
    '''
    for labelme_file in tqdm.tqdm(os.listdir(labelme_folder)):
        if not labelme_file.endswith(".json"):
            continue
        file_key = get_file_key(labelme_file)
        labelme_path = os.path.join(labelme_folder, labelme_file)
        labelme_dict = json_load(labelme_path)
        image_path = labelme_path.replace(".json", ".png")
        image = cv2_imread(image_path)
        image_height, image_width = image.shape[:2]
        bboxes = labelme2std(labelme_dict)
        image_name = labelme_dict["imagePath"]
        bboxes_new = []
        for i, bbox in enumerate(bboxes):
            class_ = get_std_box_class(bbox)
            # try:
            if True:
                class_ = map_func(class_)
                if class_ is None:
                    continue
                set_std_box_class(bbox, class_)
                bboxes_new.append(bbox)
            # except Exception as e:
            #     print(f"v3_class_check error: {e} on {class_}")
            #     continue
        bboxes = bboxes_new
        if output_folder is not None:
            labelme_path_ = ensure_parent(
                pathj(output_folder, labelme_file))
            image_path_ = labelme_path_.replace(".json", ".png")
            copy2(image_path, image_path_)
            Labelme_res.from_std(
                bboxes, image_name, image_width, image_height).dump(labelme_path_)


def modify_labelme_script(input_folder, output_folder, map_func):
    # output_folder = ensure_dir(input_folder + "crop_sub")
    if output_folder is None:
        output_folder = ensure_dir(input_folder + "_modify_labelme_script")
    for software_i in tqdm.tqdm(os.listdir(input_folder), desc="modify_labelme_script"):
        software_i_path = os.path.join(input_folder, software_i, "imgs")
        if not os.path.isdir(software_i_path):
            continue
        # crop_sub_script_i(software_i_path, output_folder=output_folder_software)

        output_folder_i = output_folder + \
            software_i_path[len(input_folder):]

        modify_labelme_script_i(
            software_i_path,  output_folder=output_folder_i, map_func=map_func)

    return


if __name__ == "__main__":
    # labelme_folder = r"E:\code_work\data\cv_product\auto_label\用采\gallery"
    # labelme_folder = r"E:\code_work\data\cv_product\auto_label\Wind合规信披\gallery"
    # labelme_folder = "/workspace/bohuang/data/button_detect_threeclass_coco/labelme"
    # labelme_check_script(labelme_folder)

    crop_folder = r"E:\code_work\data\cv_product\form\2022.9.20_前场国网\pure_form\label"
    crop_folder = r"E:\code_work\data\cv_product\form\2022.9.20_前场国网\pure_form\label\all_0930\orig\form_kv_data_results_flatten"
    # crop_sub_script(crop_folder)
    crop_folder = r"E:\code_work\data\cv_product\图标细分类\图标细分类"
    crop_folder = r"E:\code_work\data\detect\0006_sa_v1.6_cleanto_0010"
    crop_sub_script(crop_folder)
