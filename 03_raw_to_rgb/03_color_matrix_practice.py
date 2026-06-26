# -*- coding: utf-8 -*-
"""
颜色校正矩阵手写练习。

这一节只练一个核心函数：
    apply_color_matrix(image_bgr, matrix)

你要自己完成这个函数，观察 3x3 矩阵如何改变图像颜色。
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

from raw_to_rgb_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "03_color_matrix_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def apply_color_matrix(image_bgr, matrix):
    """
    功能：
    把每个像素的 [B, G, R] 乘一个 3x3 颜色矩阵。

    你要完成的步骤：
    1. 把 image_bgr 转成 float32，并除以 255.0
    2. 用 @ 做矩阵乘法
    3. 用 np.clip 把结果限制在 0.0 到 1.0
    4. 乘回 255.0，并转成 uint8
    """
    image_float = image_bgr.astype(np.float32) / 255.0
    corrected = image_float @ matrix.T
    corrected = np.clip(corrected, 0.0, 1.0)
    return (corrected * 255.0).astype(np.uint8)


def main():
    """读取图片，调用你的颜色矩阵函数，并保存对比图。"""
    parser = argparse.ArgumentParser(description="Color matrix practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    args = parser.parse_args()

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=420)

    identity_matrix = np.array(
        [
            [1.00, 0.00, 0.00],
            [0.00, 1.00, 0.00],
            [0.00, 0.00, 1.00],
        ],
        dtype=np.float32,
    )

    warm_matrix = np.array(
        [
            [0.95, 0.00, 0.00],
            [0.00, 1.00, 0.00],
            [0.00, 0.04, 1.08],
        ],
        dtype=np.float32,
    )

    cool_matrix = np.array(
        [
            [1.12, 0.03, 0.00],
            [0.00, 1.00, 0.00],
            [0.00, 0.00, 0.92],
        ],
        dtype=np.float32,
    )

    identity = apply_color_matrix(image_bgr, identity_matrix)
    warm = apply_color_matrix(image_bgr, warm_matrix)
    cool = apply_color_matrix(image_bgr, cool_matrix)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_identity.png"), identity)
    cv2.imwrite(str(output_dir / "03_warm.png"), warm)
    cv2.imwrite(str(output_dir / "04_cool.png"), cool)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=260),
            add_label(identity, "Identity", label_width=260),
            add_label(warm, "Warm", label_width=260),
            add_label(cool, "Cool", label_width=260),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("已保存: compare.png")


if __name__ == "__main__":
    main()
