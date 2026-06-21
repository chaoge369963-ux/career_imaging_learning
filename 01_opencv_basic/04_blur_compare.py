# -*- coding: utf-8 -*-
"""
第四课：比较均值模糊和高斯模糊。

运行方式：
    python 01_opencv_basic/04_blur_compare.py
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
image_path = script_dir / "outputs" / "01_read_gray_hist" / "original.png"
output_dir = script_dir / "outputs" / "04_blur_compare"
output_dir.mkdir(parents=True, exist_ok=True)


def add_label(image_bgr, label):
    """在图片左上角写一个标签，方便看对比图。"""
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


def main():
    """读取图片，分别做均值模糊和高斯模糊。"""
    image_bgr = cv2.imread(str(image_path))

    if image_bgr is None:
        raise FileNotFoundError("图片读取失败，请先运行 01_read_gray_hist.py 生成 original.png")

    print("原图 shape:", image_bgr.shape)

    # 核大小可以理解为“看周围多大一片区域来做模糊”。
    # 数字越大，模糊越强；高斯模糊的核大小必须是奇数，比如 3、5、7、9。
    kernel_size = (21, 21)

    # TODO: 这两行是本课核心。
    # 均值模糊：把邻域内的像素简单求平均。
    mean_blur = cv2.blur(image_bgr, kernel_size)

    # 高斯模糊：离中心越近的像素权重越大，通常比均值模糊更自然。
    gaussian_blur = cv2.GaussianBlur(image_bgr, kernel_size, 0)

    print("均值模糊 shape:", mean_blur.shape)
    print("高斯模糊 shape:", gaussian_blur.shape)

    original_path = output_dir / "original1.png"
    mean_path = output_dir / "mean_blur1.png"
    gaussian_path = output_dir / "gaussian_blur1.png"
    compare_path = output_dir / "compare1.png"

    cv2.imwrite(str(original_path), image_bgr)
    cv2.imwrite(str(mean_path), mean_blur)
    cv2.imwrite(str(gaussian_path), gaussian_blur)

    # 把三张图横向拼在一起，方便直接比较。
    compare = np.hstack(
        [
            add_label(image_bgr, "Original"),
            add_label(mean_blur, "Mean Blur"),
            add_label(gaussian_blur, "Gaussian Blur"),
        ]
    )
    cv2.imwrite(str(compare_path), compare)

    print("保存原图:", original_path)
    print("保存均值模糊:", mean_path)
    print("保存高斯模糊:", gaussian_path)
    print("保存对比图:", compare_path)


if __name__ == "__main__":
    main()
