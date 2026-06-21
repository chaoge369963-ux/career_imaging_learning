# -*- coding: utf-8 -*-
"""
第五课：用卷积核做图像锐化。

运行方式：
    python 01_opencv_basic/05_sharpen_kernel.py

本课你要自己补的核心函数：
    apply_sharpen_kernel(image_bgr)
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
image_path = script_dir / "outputs" / "01_read_gray_hist" / "original.png"
output_dir = script_dir / "outputs" / "05_sharpen_kernel"
output_dir.mkdir(parents=True, exist_ok=True)


def add_label(image_bgr, label):
    """在图片左上角写标签，方便看对比图。"""
    labeled = image_bgr.copy()
    cv2.putText(
        labeled,
        label,
        (16, 32),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    return labeled


def apply_sharpen_kernel(image_bgr):
    """用锐化卷积核处理图片。

    你要在这里完成 3 件事：
    1. 创建一个 3 x 3 的锐化 kernel。
    2. 用 cv2.filter2D 把 kernel 作用到 image_bgr 上。
    3. return 锐化后的图片。
    """
    # TODO: 你来写这里。
    
    # 提示 1：锐化 kernel 可以先用这个：
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0],
    ], dtype=np.float32)
    #
    # 提示 2：OpenCV 里应用卷积核：
    sharpened = cv2.filter2D(image_bgr, -1, kernel)
    #
    # 提示 3：最后 return sharpened
    # raise NotImplementedError("请先补完 apply_sharpen_kernel(image_bgr)")
    return sharpened


def main():
    """读取图片，调用你写的锐化函数，并保存结果。"""
    image_bgr = cv2.imread(str(image_path))

    if image_bgr is None:
        raise FileNotFoundError("图片读取失败，请先运行 01_read_gray_hist.py 生成 original.png")

    print("原图 shape:", image_bgr.shape)
    kernel_size = (5, 5)
    blurred = cv2.blur(image_bgr, kernel_size)


    sharpened = apply_sharpen_kernel(blurred)

    print("锐化图 shape:", sharpened.shape)
    print("原图 dtype:", image_bgr.dtype)
    print("锐化图 dtype:", sharpened.dtype)

    original_path = output_dir / "original.png"
    blurred_path = output_dir / "blurred.png"
    sharpened_path = output_dir / "sharpened.png"
    compare_path = output_dir / "compare.png"

    cv2.imwrite(str(original_path), image_bgr)
    cv2.imwrite(str(blurred_path), blurred)
    cv2.imwrite(str(sharpened_path), sharpened)

    compare = np.hstack(
        [
            add_label(image_bgr, "Original"),
            add_label(blurred, "Blurred"),
            add_label(sharpened, "Sharpened"),
        ]
    )
    cv2.imwrite(str(compare_path), compare)

    print("保存原图:", original_path)
    print("保存模糊图:", blurred_path)
    print("保存锐化图:", sharpened_path)
    print("保存对比图:", compare_path)


if __name__ == "__main__":
    main()
