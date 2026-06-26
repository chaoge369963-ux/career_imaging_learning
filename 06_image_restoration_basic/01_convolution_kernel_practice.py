# -*- coding: utf-8 -*-
"""
传统图像复原第 1 课：卷积核练习。

这一课只抓一个核心：
    图像滤波 = 用一个小矩阵 kernel 在图像上滑动，重新计算每个像素。

你这次要自己完成 make_box_kernel()。
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

from restoration_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "01_convolution_kernel_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def make_box_kernel(kernel_size):
    """
    功能：
    创建一个均值滤波卷积核。

    例子：
    kernel_size = 3 时，返回一个 3x3 矩阵，每个值都是 1/9。


    """

    kernel = np.ones([kernel_size,kernel_size])
    kernel = kernel.astype(np.float32)
    kernel = kernel/kernel_size**2
    return kernel
    raise NotImplementedError("请你自己完成 make_box_kernel()")


def apply_kernel(image_bgr, kernel):
    """用 OpenCV 的 filter2D 对图像应用卷积核。"""
    return cv2.filter2D(image_bgr, -1, kernel, borderType=cv2.BORDER_REFLECT)


def make_sharpen_kernel():
    """创建一个简单锐化卷积核。"""
    return np.array(
        [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0],
        ],
        dtype=np.float32,
    )


def print_kernel(name, kernel):
    """打印卷积核，观察它的形状和数值和。"""
    print(name)
    print(kernel)
    print("shape:", kernel.shape, "sum:", float(kernel.sum()))


def main():
    """读取图片，分别做均值模糊和锐化，保存对比图。"""
    parser = argparse.ArgumentParser(description="Convolution kernel practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--kernel-size", type=int, default=5, help="均值滤波核大小")
    args = parser.parse_args()

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=420)

    box_kernel = make_box_kernel(args.kernel_size)
    sharpen_kernel = make_sharpen_kernel()

    print_kernel("box kernel", box_kernel)
    print_kernel("sharpen kernel", sharpen_kernel)

    blurred = apply_kernel(image_bgr, box_kernel)
    sharpened = apply_kernel(image_bgr, sharpen_kernel)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_box_blur.png"), blurred)
    cv2.imwrite(str(output_dir / "03_sharpen.png"), sharpened)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=260),
            add_label(blurred, "Box Blur", label_width=260),
            add_label(sharpened, "Sharpen", label_width=260),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("已保存: compare.png")


if __name__ == "__main__":
    main()
