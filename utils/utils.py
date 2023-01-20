import json
import yaml
import pandas as pd
import os
import torch
from typing import Any, List, Optional, Tuple, Type, Union
import numpy as np
import cv2
#json yaml

def read_json_instance(name):
    print(name)
    return json.load(name)

def save_json_instance(content_path, save):
    with open(content_path, 'w', encoding='utf-8') as f:
        json.dump(save, f, ensure_ascii=False, indent=2)

        
def read_yaml_instance(name):
    return yaml.load()

def save_yaml_instance(content_path, save):
    with open(content_path, 'w') as file:
        file.write(yaml.dump(save, allow_unicode=True))

def dir_names(file_path):
    img_list = [x for x in os.listdir(file_path)]
    return img_list


def convert_overlay_heatmap(feat_map: Union[np.ndarray, torch.Tensor],
                            img: Optional[np.ndarray] = None,
                            alpha: float = 0.5) -> np.ndarray:
    """Convert feat_map to heatmap and overlay on image, if image is not None.

    Args:
        feat_map (np.ndarray, torch.Tensor): The feat_map to convert
            with of shape (H, W), where H is the image height and W is
            the image width.
        img (np.ndarray, optional): The origin image. The format
            should be RGB. Defaults to None.
        alpha (float): The transparency of featmap. Defaults to 0.5.

    Returns:
        np.ndarray: heatmap
    """
    assert feat_map.ndim == 2 or (feat_map.ndim == 3
                                  and feat_map.shape[0] in [1, 3])
    if isinstance(feat_map, torch.Tensor):
        feat_map = feat_map.detach().cpu().numpy()

    if feat_map.ndim == 3:
        feat_map = feat_map.transpose(1, 2, 0)

    norm_img = np.zeros(feat_map.shape)
    norm_img = cv2.normalize(feat_map, norm_img, 0, 255, cv2.NORM_MINMAX)
    norm_img = np.asarray(norm_img, dtype=np.uint8)
    heat_img = cv2.applyColorMap(norm_img, cv2.COLORMAP_JET)
    heat_img = cv2.cvtColor(heat_img, cv2.COLOR_BGR2RGB)
    if img is not None:
        heat_img = cv2.addWeighted(img, 1 - alpha, heat_img, alpha, 0) #叠加热力图
    return heat_img