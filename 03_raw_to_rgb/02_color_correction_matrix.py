# -*- coding: utf-8 -*-
"""
颜色校正矩阵练习：观察 3x3 矩阵如何改变图像颜色。

运行方式：
    python 03_raw_to_rgb/02_color_correction_matrix.py

使用自己的图片：
    python 03_raw_to_rgb/02_color_correction_matrix.py --image C:/path/to/image.png
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

from raw_to_rgb_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "02_color_correction_matrix"
output_dir.mkdir(parents=True, exist_ok=True)


def apply_color_matrix(image_bgr, matrix):
    """对每个像素的 BGR 三个通道乘 3x3 颜色矩阵。"""
    image_float = image_bgr.astype(np.float32) / 255.0

    # image_float 的形状是 H x W x 3，matrix.T 的形状是 3 x 3。
    # @ 表示矩阵乘法：每个像素的 [B, G, R] 都会被重新混合。
    corrected = image_float @ matrix.T

    corrected = np.clip(corrected, 0.0, 1.0)
    return (corrected * 255.0).astype(np.uint8)


def print_image_info(name, image_bgr):
    """打印 shape、dtype、最小值、最大值，训练你观察数组。"""
    print(
        name,
        "shape:",
        image_bgr.shape,
        "dtype:",
        image_bgr.dtype,
        "min:",
        image_bgr.min(),
        "max:",
        image_bgr.max(),
    )


def main():
    """运行颜色校正矩阵练习，并保存结果图。"""
    parser = argparse.ArgumentParser(description="Color correction matrix demo")
    parser.add_argument("--image", type=str, default=None, help="输入图片路径")
    args = parser.parse_args()

    if args.image is None:
        image_path = default_image_path
    else:
        image_path = Path(args.image)

    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr)
    print_image_info("input", image_bgr)

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

    vivid_matrix = np.array(
        [
            [1.08, -0.04, -0.02],
            [-0.03, 1.08, -0.03],
            [-0.02, -0.04, 1.10],
        ],
        dtype=np.float32,
    )

    identity = apply_color_matrix(image_bgr, identity_matrix)
    warm = apply_color_matrix(image_bgr, warm_matrix)
    cool = apply_color_matrix(image_bgr, cool_matrix)
    vivid = apply_color_matrix(image_bgr, vivid_matrix)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_identity.png"), identity)
    cv2.imwrite(str(output_dir / "03_warm.png"), warm)
    cv2.imwrite(str(output_dir / "04_cool.png"), cool)
    cv2.imwrite(str(output_dir / "05_vivid.png"), vivid)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=280),
            add_label(identity, "Identity", label_width=280),
            add_label(warm, "Warm", label_width=280),
            add_label(cool, "Cool", label_width=280),
            add_label(vivid, "Vivid", label_width=280),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("已保存: 01_input.png 到 05_vivid.png，以及 compare.png")


if __name__ == "__main__":
    main()
