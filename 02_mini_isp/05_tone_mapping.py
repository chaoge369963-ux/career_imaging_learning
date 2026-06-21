# -*- coding: utf-8 -*-
"""
mini ISP 第五课：Tone Mapping。

运行方式：
    python 02_mini_isp/05_tone_mapping.py

本课核心函数：
    apply_reinhard_tone_mapping(image_bgr, exposure)
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
input_dir = script_dir / "outputs" / "04_gamma_correction"
output_dir = script_dir / "outputs" / "05_tone_mapping"
output_dir.mkdir(parents=True, exist_ok=True)

input_path = input_dir / "gamma_1.0.png"


def add_label(image_bgr, label):
    """在图片左上角写标签，方便看对比图。"""
    labeled = image_bgr.copy()
    cv2.rectangle(labeled, (0, 0), (300, 42), (255, 255, 255), thickness=-1)
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


def create_bright_image(image_bgr):
    """人为制造一张过亮图，模拟需要 tone mapping 的情况。"""
    image_float = image_bgr.astype(np.float32) / 255.0
    bright_float = image_float * 2.8

    preview = np.clip(bright_float * 255.0, 0, 255).astype(np.uint8)
    return bright_float, preview


def apply_reinhard_tone_mapping(image_bgr, exposure):
    """对 BGR 图像做简单 Reinhard tone mapping，返回 uint8 图像。"""
    x = image_bgr.astype(np.float32)*exposure
    mapped = np.clip((x/(1+x))*255,0,255)
    return mapped.astype(np.uint8)


def main():
    """读取 gamma 图，制造过亮图，再做 tone mapping。"""
    image_bgr = cv2.imread(str(input_path), cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise FileNotFoundError("找不到 gamma_1.0.png，请先运行 02_mini_isp/04_gamma_correction.py")

    print("输入图 shape:", image_bgr.shape)
    print("输入图 dtype:", image_bgr.dtype)

    bright_float, bright_preview = create_bright_image(image_bgr)
    tone_mapped = apply_reinhard_tone_mapping(bright_float, exposure=1.0)

    print("过亮预览 shape:", bright_preview.shape)
    print("Tone mapped shape:", tone_mapped.shape)
    print("Tone mapped dtype:", tone_mapped.dtype)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input"),
            add_label(bright_preview, "Over Bright"),
            add_label(tone_mapped, "Tone Mapped"),
        ]
    )

    cv2.imwrite(str(output_dir / "input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "over_bright_preview.png"), bright_preview)
    cv2.imwrite(str(output_dir / "tone_mapped.png"), tone_mapped)
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输出目录:", output_dir)
    print("已保存: input.png, over_bright_preview.png, tone_mapped.png, compare.png")


if __name__ == "__main__":
    main()
