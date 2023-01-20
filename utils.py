import json
import math
from cv2 import exp
import numpy as np
from pypinyin import pinyin, NORMAL
import os

def word_to_pinyin(word: str):
    '''
    :param word: 输入的中文字符串
    :return: 英文字符串
    '''
    s = ''
    for i in pinyin(word, style=NORMAL):
        s += i[0].strip()
    return s

# -----以下代码用来进行坐标转换-----
def extract_xys(axiss):
    '''
    :param axiss: xml文件中的坐标系父节点
    :return: points[x1,y1,...,xn,yn]
    '''
    return [float(axis.text) for axis in axiss]

def points_to_xywh(points: list):
    '''
    :param points: labelme json points坐标系
    :return: box左上坐标+wh
    '''
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return min_x, min_y, max_x-min_x, max_y-min_y
# -----以上代码用来进行坐标转换-----

# -----以下代码求两线段交点坐标-----
class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line(object):
    # a=0, b=0, c=0
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

def getLinePara(line):
    line.a =line.p1.y - line.p2.y;
    line.b = line.p2.x - line.p1.x;
    line.c = line.p1.x *line.p2.y - line.p2.x * line.p1.y;

def getCrossPoint(l1, l2):
    getLinePara(l1);
    getLinePara(l2);
    d = l1.a * l2.b - l2.a * l1.b
    p=Point()
    if d == 0: return None
    p.x = (l1.b * l2.c - l2.b * l1.c)*1.0 / d
    p.y = (l1.c * l2.a - l2.c * l1.a)*1.0 / d
    return p;

def get_cross_point(x1, y1, x2, y2, x3, y3, x4, y4):
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)
    l1 = Line(p1, p2)
    p3 = Point(x3, y3)
    p4 = Point(x4, y4)
    l2 = Line(p3, p4)
    cp = getCrossPoint(l1, l2)
    if cp == None \
            or cp.x < min([x1, x2])-0.01 \
            or cp.x > max([x1, x2])+0.01 \
            or cp.y < min([y1, y2])-0.01 \
            or cp.y > max([y1, y2])+0.01 \
            or cp.x < min([x3, x4])-0.01 \
            or cp.x > max([x3, x4])+0.01 \
            or cp.y < min([y3, y4])-0.01 \
            or cp.y > max([y3, y4])+0.01:
        return None
    else:
        return [cp.x, cp.y]
# -----以上求两线段交点坐标-----

def json_to_instance(json_file_path: str):
    '''
    :param json_file_path: json文件路径
    :return: json instance
    '''
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    return instance

def instance_to_json(instance, json_file_path: str):
    '''
    :param instance: json instance
    :param json_file_path: 保存为json的文件路径
    :return: 将json instance保存到相应文件路径
    '''
    with open(json_file_path, 'w', encoding='utf-8') as f:
        content = json.dumps(instance)
        f.write(content)

def get_edge(img, thres=20):
    '''
    :param img: cv2读取的img对象
    :param thres: 读到图片边缘像素的跳越阈值
    :return: 图片中目标上下左右的坐标值
    '''
    result = []
    h, w, c = img.shape
    for i in range(h):
        if img[i, int(w/2), 0] >= thres:
            break
    result.append(i)
    for i in reversed(range(h)):
        if img[i-1, int(w/2), 0] >= thres:
            break
    result.append(i)
    for i in range(w):
        if img[int(h/2), i, 0] >= thres:
            break
    result.append(i)
    for i in reversed(range(w)):
        if img[int(h/2), i-1, 0] >= thres:
            break
    result.append(i)
    return result

def points_to_coco_bbox(points, shape_type):
    '''
    :param points: labelme json中的points[[x1,y1],[x2,y2],...，[xn,yn]]
    :param shape_type: 例如'circle', 'point', 'line', 'linestrip'
    :return: coco bbox[xmin,ymin,w,h]
    '''
    if shape_type == 'circle':
        center = [points[0][0], points[0][1]]
        radius = math.sqrt((points[1][0]-center[0])**2+(points[1][1]-center[1])**2)
        result = [center[0]-radius, center[1]-radius, 2*radius, 2*radius]
    elif shape_type == 'point':
        result = [points[0][0]-1, points[0][1]-1, 3, 3]
    else:
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        min_x, min_y = min(xs), min(ys)
        max_x, max_y = max(xs), max(ys)
        result = [min_x, min_y, max_x-min_x, max_y-min_y]
    return result

def points_to_coco_segmentation(points, shape_type, line_pixel=1):
    '''
    :param points: labelme json中的points[[x1,y1],[x2,y2],...[xn,yn]]
    :param shape_type: 例如'circle', 'point', 'line', 'linestrip'
    :param line_pixel: labelme中line、linestrip points的加宽像素值
    :return: coco segmentation[[x1,y1,x2,y2,...,xn,yn]]
    '''
    if shape_type == 'rectangle':
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        min_x, min_y = min(xs), min(ys)
        max_x, max_y = max(xs), max(ys)
        result = [[min_x, min_y, max_x, min_y, max_x, max_y, min_x, max_y]]
    elif shape_type == 'circle':
        center = [points[0][0], points[0][1]]
        radius = math.sqrt((points[1][0]-center[0])**2+(points[1][1]-center[1])**2)
        temp = []
        for i in range(0, 360, 10):
            temp.append(center[0]+math.cos(math.pi*i/180)*radius)
            temp.append(center[1]+math.sin(math.pi*i/180)*radius)
        result = [temp]
    elif shape_type == 'line' or shape_type == 'linestrip':
        result = [line_pixel_widen(points, line_pixel)]
    else:
        result = [np.asarray(points).flatten().tolist()]
    return result

def line_pixel_widen(points, pixel=1):
    '''
    :param points: labelme中标签为line、linestrip的points
    :param pixel: 加宽的像素点
    :return: 返回coco中直线segmentation的坐标点
    '''
    line1 = []
    line2 = []
    for i, point in enumerate(points):
        if i == 0:
            vector2 = (points[i+1][0] - point[0], points[i+1][1] - point[1])
            angle_horiz = get_horiz_angle(vector2) + math.pi/2
            line1.append(perturbation_around_point(point, angle_horiz, pixel)[0])
            line2.append(perturbation_around_point(point, angle_horiz, pixel)[1])
        elif i == len(points)-1:
            vector1 = (points[i-1][0] - point[0], points[i-1][1] - point[1])
            angle_horiz = get_horiz_angle(vector1) + math.pi/2
            perturb_points = perturbation_around_point(point, angle_horiz, pixel)
            if get_cross_point(points[i-1][0], points[i-1][1], points[i][0], points[i][1], perturb_points[0][0], perturb_points[0][1], line1[-1][0], line1[-1][1]) == None:
                line1.append(perturb_points[0])
                line2.append(perturb_points[1])
            else:
                line1.append(perturb_points[1])
                line2.append(perturb_points[0])
        else:
            vector1 = (points[i-1][0] - point[0], points[i-1][1] - point[1])
            vector2 = (points[i+1][0] - point[0], points[i+1][1] - point[1])
            angle_horiz = get_mid_horiz_angle(vector1, vector2)
            perturb_points = perturbation_around_point(point, angle_horiz, pixel)
            if get_cross_point(points[i-1][0], points[i-1][1], points[i][0], points[i][1], perturb_points[0][0], perturb_points[0][1], line1[-1][0], line1[-1][1]) == None:
                line1.append(perturb_points[0])
                line2.append(perturb_points[1])
            else:
                line1.append(perturb_points[1])
                line2.append(perturb_points[0])
    return np.asarray(line1.extend(reversed(line2))).flatten().tolist()
 
def ensure_parent(path):
    folder, name = os.path.split(path)
    if folder:
        ensure_dir(folder)
    return path

def ensure_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

def perturbation_around_point(point, angle, pixel):
    '''
    :param point: 目标坐标点
    :param angle: 微扰角度
    :param pixel: 微扰幅度
    :return: 返回一个坐标点的周围两个微扰点
    '''
    return [point[0]+pixel*math.cos(angle), point[1]+pixel*math.sin(angle)],\
           [point[0]-pixel*math.cos(angle), point[1]-pixel*math.sin(angle)]

def get_mid_horiz_angle(vector1, vector2):
    '''
    :param vector1: 向量1
    :param vector2: 向量2
    :return: 两个向量的中间向量与水平线(1,0)的夹角
    '''
    angle_horiz_1 = get_horiz_angle(vector1)
    angle_horiz_2 = get_horiz_angle(vector2)
    return (angle_horiz_1 + angle_horiz_2)/2

def get_horiz_angle(vector):
    '''
    :param vector: 一个向量
    :return: 该向量和水平线(1,0)的夹角(-180-180)
    '''
    angle_horiz = get_angle((1, 0), vector) if vector[1] > 0 else -get_angle((1, 0), vector)
    return angle_horiz

def get_angle(vector1, vector2):
    '''
    :param vector1: 向量1
    :param vector2: 向量2
    :return: 向量之间的夹角(0-180)
    '''
    inner_product = vector1[0]*vector2[0] + vector1[1]*vector2[1]
    cosin = inner_product/(math.sqrt((vector1[0]**2+vector1[1]**2)*(vector2[0]**2+vector2[1]**2)))
    return math.acos(cosin)

def instance_points_to_polygon(instance):
    '''
    :param instance: labelme json instance
    :return: 将instance['shapes']中points的标签，由rectangle和circle变为polygon，从而更好地进行crop和fill
    '''
    objs = instance['shapes']
    for obj in objs:
        shape_type = obj['shape_type']
        points = obj['points']
        if shape_type == 'retangle':
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            min_x, min_y = min(xs), min(ys)
            max_x, max_y = max(xs), max(ys)
            obj['points'] = [[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]]
            obj['shape_type'] = 'polygon'
        elif shape_type == 'circle':
            center = [points[0][0], points[0][1]]
            radius = math.sqrt((points[1][0]-center[0])* 2+(points[1][1]-center[1])**2)
            obj['points'] = []
            obj['shape_type'] = 'polygon'
            for i in range(0, 360, 10):
                obj['points'].append([center[0]+math.cos(math.pi*i/180)*radius, center[1]+math.sin(math.pi*i/180)*radius])

def crop_is_empty(instance, crop_size, iou_thres=0.2):
    '''
    :param instance: labelme json instance
    :param crop_size: crop范围[上，下，左，右]
    :return: bool值
    '''
    flag = True
    for obj in instance['shapes']:
        points = obj['points']
        if obj_in_crop(points, crop_size, iou_thres):
            flag = False
            break
    return flag

def obj_in_crop(points, crop_size, iou_thres=0.2):
    '''
    :param points: labelme json中一个obj的points
    :param crop_size: crop范围[上，下，左，右]
    :param iou_thres: iou阈值
    :return: bool值
    '''
    crop_box = Box(crop_size[2], crop_size[0], crop_size[3] - crop_size[2], crop_size[1] - crop_size[0])
    x, y, w, h = points_to_xywh(points)
    obj_box = Box(x, y, w, h)
    inter_area = calculate_inter_area(obj_box, crop_box)
    return inter_area != 0 and inter_area/obj_box >= iou_thres

def point_in_crop(point, crop_size):
    '''
    :param point: labelme json中一个obj的points-point[x,y]
    :param crop_size: crop范围[上，下，左，右]
    :return: bool值
    '''
    return point[0] > crop_size[2] and \
           point[0] < crop_size[3] and \
           point[1] > crop_size[0] and \
           point[1] < crop_size[1]

# -----以下代码为数据增强部分-----
class Box:
    # xy是左上角坐标
    def __init__(self, x, y, w, h, category=None, confidence=None):
        self.category = category
        self.confidence = confidence
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_area(self):
        return self.w * self.h

    def get_iou(self, box2):
        inter_area = calculate_inter_area(self, box2)
        
        try:
            return inter_area/(self.get_area()+box2.get_area()-inter_area)
        except:
            return 0

def calculate_inter_area(box1, box2):
    '''
    :param box1: Box对象
    :param box2: Box对象
    :return: box1与box2的交面积
    '''
    left_x, left_y = max([box1.x, box2.x]), max([box1.y, box2.y])
    right_x, right_y = min([box1.x + box1.w, box2.x + box2.w]), min([box1.y + box1.h, box2.y + box2.h])
    height = right_y - left_y
    width = right_x - left_x
    area = height * width if height>0 and width>0 else 0
    return area
# -----以上代码为数据增强部分-----

# if __name__ == '__main__':
    # print(perturbation_around_point([1,1], -1.57/2, 1.414))

























