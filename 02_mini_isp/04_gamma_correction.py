# -*- coding: utf-8 -*-
"""
mini ISP 第四课：Gamma Correction。

运行方式：
    python 02_mini_isp/04_gamma_correction.py

本课核心函数：
    apply_gamma(image_bgr, gamma)
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
input_dir = script_dir / "outputs" / "03_white_balance"
output_dir = script_dir / "outputs" / "04_gamma_correction"
output_dir.mkdir(parents=True, exist_ok=True)

input_path = input_dir / "white_balance.png"


def add_label(image_bgr, label):
    """在图片左上角写标签，方便看对比图。"""
    labeled = image_bgr.copy()
    cv2.rectangle(labeled, (0, 0), (260, 42), (255, 255, 255), thickness=-1)
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


def apply_gamma(image_bgr, gamma):
    """对 BGR 图像做 gamma correction，返回处理后的 uint8 图像。"""
    image_float = image_bgr.astype(np.float32) / 255.0
    corrected = image_float ** gamma
    corrected = np.clip(corrected * 255.0, 0, 255)
    return corrected.astype(np.uint8)


def main():
    """读取白平衡图，尝试不同 gamma 值，并保存结果。"""
    image_bgr = cv2.imread(str(input_path), cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise FileNotFoundError("找不到 white_balance.png，请先运行 02_mini_isp/03_white_balance.py")

    print("输入图 shape:", image_bgr.shape)
    print("输入图 dtype:", image_bgr.dtype)

    gamma_values = [0.5, 1.0, 2.2]
    gamma_images = []

    for gamma in gamma_values:
        corrected = apply_gamma(image_bgr, gamma)
        gamma_images.append(corrected)
        cv2.imwrite(str(output_dir / f"gamma_{gamma}.png"), corrected)
        print(f"gamma={gamma}, 输出 dtype:", corrected.dtype, "shape:", corrected.shape)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input"),
            add_label(gamma_images[0], "Gamma 0.5"),
            add_label(gamma_images[1], "Gamma 1.0"),
            add_label(gamma_images[2], "Gamma 2.2"),
        ]
    )

    cv2.imwrite(str(output_dir / "input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输出目录:", output_dir)
    print("已保存: input.png, gamma_0.5.png, gamma_1.0.png, gamma_2.2.png, compare.png")


if __name__ == "__main__":
    main()
