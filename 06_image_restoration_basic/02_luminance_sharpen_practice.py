# -*- coding: utf-8 -*-
"""
传统图像复原第 2 课：直接锐化 BGR vs 只锐化亮度。

这节课回答你刚才的问题：
    锐化会不会改变颜色？

直接对 B/G/R 三个通道锐化，可能让颜色比例改变。
只对亮度通道 Y 锐化，通常更不容易改颜色。
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

from restoration_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "02_luminance_sharpen_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def make_4_neighbor_sharpen_kernel():
    """4 邻域锐化核：只看上下左右。"""
    return np.array(
        [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0],
        ],
        dtype=np.float32,
    )


def make_8_neighbor_sharpen_kernel():
    """
    功能：
    创建 8 邻域锐化核。

    你要返回：
    [
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1],
    ]
    """
    return np.array(
        [
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1],
        ],
        dtype=np.float32,
    )


def sharpen_bgr_direct(image_bgr, kernel):
    """直接对 B/G/R 三个通道锐化。"""
    return cv2.filter2D(image_bgr, -1, kernel, borderType=cv2.BORDER_REFLECT)


def sharpen_luminance_only(image_bgr, kernel):
    """
    功能：
    只锐化亮度 Y 通道，再转回 BGR。

  
    """
    image_ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(image_ycrcb)
    y_sharp = cv2.filter2D(y, -1, kernel, borderType=cv2.BORDER_REFLECT)
    sharp_ycrcb = cv2.merge((y_sharp, cr, cb))
    return cv2.cvtColor(sharp_ycrcb, cv2.COLOR_YCrCb2BGR)


def print_kernel(name, kernel):
    """打印卷积核，观察它的形状和数值和。"""
    print(name)
    print(kernel)
    print("shape:", kernel.shape, "sum:", float(kernel.sum()))


def main():
    """读取图片，对比直接彩色锐化和只锐化亮度。"""
    parser = argparse.ArgumentParser(description="Luminance sharpen practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--kernel-type", choices=["4", "8"], default="8", help="锐化核类型")
    args = parser.parse_args()

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=380)

    if args.kernel_type == "8":
        kernel = make_8_neighbor_sharpen_kernel()
    else:
        kernel = make_4_neighbor_sharpen_kernel()

    print_kernel("sharpen kernel", kernel)

    bgr_sharpen = sharpen_bgr_direct(image_bgr, kernel)
    y_sharpen = sharpen_luminance_only(image_bgr, kernel)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_bgr_direct_sharpen.png"), bgr_sharpen)
    cv2.imwrite(str(output_dir / "03_luminance_only_sharpen.png"), y_sharpen)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=250),
            add_label(bgr_sharpen, "BGR Sharpen", label_width=280),
            add_label(y_sharpen, "Y-only Sharpen", label_width=300),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("已保存: compare.png")


if __name__ == "__main__":
    main()
