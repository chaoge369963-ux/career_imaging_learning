# -*- coding: utf-8 -*-
"""传统图像复原阶段共用的小工具函数。"""

from pathlib import Path

import cv2
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_IMAGE_PATH = Path(r"C:\Users\magic\Pictures\web图片\OIP.png")
FALLBACK_IMAGE_PATH = PROJECT_DIR / "01_opencv_basic" / "outputs" / "01_read_gray_hist" / "original.png"


def get_default_image_path():
    """优先使用你的 OIP 图片；如果不存在，就退回到项目里的练习图。"""
    if DEFAULT_IMAGE_PATH.exists():
        return DEFAULT_IMAGE_PATH
    return FALLBACK_IMAGE_PATH


def read_image_bgr(image_path):
    """读取图片，并兼容 Windows 中文路径。"""
    image_bytes = np.fromfile(str(image_path), dtype=np.uint8)
    image_bgr = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    return image_bgr


def resize_for_demo(image_bgr, max_width=420):
    """把过大的输入图缩小，方便横向拼接观察。"""
    height, width = image_bgr.shape[:2]
    if width <= max_width:
        return image_bgr

    scale = max_width / width
    new_size = (max_width, int(height * scale))
    return cv2.resize(image_bgr, new_size, interpolation=cv2.INTER_AREA)


def add_label(image_bgr, label, label_width=260):
    """在图片左上角写标签，方便观察对比图。"""
    labeled = image_bgr.copy()
    cv2.rectangle(labeled, (0, 0), (label_width, 42), (255, 255, 255), thickness=-1)
    cv2.putText(
        labeled,
        label,
        (12, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    return labeled
