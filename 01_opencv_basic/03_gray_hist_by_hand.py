# -*- coding: utf-8 -*-
"""
第三课：自己手写读图、转灰度、保存灰度图。

运行方式：
    python 01_opencv_basic/03_gray_hist_by_hand.py
"""

from pathlib import Path

import cv2

import matplotlib.pyplot as plt

# 当前脚本所在目录，也就是 01_opencv_basic。
script_dir = Path(__file__).resolve().parent

# 读取第一课保存出来的原图。
image_path = script_dir / "outputs" / "01_read_gray_hist" / "original.png"

# 第三课的输出目录。
output_dir = script_dir / "outputs" / "03_gray_hist_by_hand"
output_dir.mkdir(parents=True, exist_ok=True)


def main():
    """读取彩色图，转成灰度图，再保存灰度图。"""
    # cv2.imread 读取图片，OpenCV 读取彩色图时默认是 BGR 顺序。
    image_bgr = cv2.imread(str(image_path))

    # 如果路径错了，image_bgr 会是 None，提前报清楚一点。
    if image_bgr is None:
        raise FileNotFoundError("图片读取失败，请检查 image_path")

    # 彩色图 shape 通常是 H x W x 3。
    print("彩色图 shape:", image_bgr.shape)

    # 把 BGR 彩色图转换成灰度图。
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # 灰度图 shape 通常是 H x W。
    print("灰度图 shape:", image_gray.shape)
    print("灰度图最暗的像素值:", image_gray.min())
    print("灰度图最亮的像素值:", image_gray.max())

    # 保存灰度图。
    gray_path = output_dir / "gray.png"
    cv2.imwrite(str(gray_path), image_gray)
    hist_path = output_dir / "histogram.png"

    plt.figure(figsize=(8, 4))
    plt.hist(image_gray.ravel(), bins=256, range=(0, 256), color="black")
    plt.title("Gray Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(str(hist_path), dpi=150)
    plt.close()

    print("保存直方图:", hist_path)
    print("保存灰度图:", gray_path)


if __name__ == "__main__":
    main()
