# -*- coding: utf-8 -*-
"""
黑电平 / 白电平 / 归一化练习。

真实 RAW 通常不是 0 到 255 的普通图片，而可能是 10-bit、12-bit、14-bit 数据。
这一节用普通图片模拟一张 12-bit RAW，让你练习：
    raw_uint16 -> subtract black level -> divide white-black -> 0.0 到 1.0
"""

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from raw_to_rgb_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "04_black_white_level_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def simulate_12bit_raw_from_gray(image_bgr, black_level, white_level):
    """用普通图片模拟 12-bit RAW：暗部不从 0 开始，而是从 black_level 开始。"""
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    gray_float = image_gray.astype(np.float32) / 255.0

    raw_float = gray_float * (white_level - black_level) + black_level
    return np.clip(raw_float, 0, 4095).astype(np.uint16)


def normalize_raw(raw_uint16, black_level, white_level):
    """
    功能：
    把模拟 12-bit RAW 归一化到 0.0 到 1.0。

    你要完成的步骤：
    1. 把 raw_uint16 转成 float32
    2. 减去 black_level
    3. 除以 (white_level - black_level)
    4. 用 np.clip 限制到 0.0 到 1.0
    5. 返回归一化后的 float32 数组
    """
    raw_float = raw_uint16.astype(np.float32)
    raw_blc = (raw_float-black_level)/(white_level-black_level)
    raw_blc = np.clip(raw_blc,0,1)
    return raw_blc



def save_histogram(raw_uint16, normalized):
    """保存归一化前后的直方图，观察数值范围变化。"""
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.hist(raw_uint16.ravel(), bins=80)
    plt.title("Raw 12-bit values")
    plt.xlabel("value")
    plt.ylabel("count")

    plt.subplot(1, 2, 2)
    plt.hist(normalized.ravel(), bins=80)
    plt.title("Normalized values")
    plt.xlabel("value")
    plt.ylabel("count")

    plt.tight_layout()
    plt.savefig(output_dir / "histogram.png", dpi=150)
    plt.close()


def main():
    """读取图片，模拟 12-bit RAW，并调用你的归一化函数。"""
    parser = argparse.ArgumentParser(description="Black/white level practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--black-level", type=float, default=256.0, help="黑电平")
    parser.add_argument("--white-level", type=float, default=4095.0, help="白电平")
    args = parser.parse_args()

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=420)
    raw_uint16 = simulate_12bit_raw_from_gray(image_bgr, args.black_level, args.white_level)
    normalized = normalize_raw(raw_uint16, args.black_level, args.white_level)

    raw_preview = (raw_uint16.astype(np.float32) / args.white_level * 255.0).astype(np.uint8)
    normalized_preview = (normalized * 255.0).astype(np.uint8)

    raw_preview_bgr = cv2.cvtColor(raw_preview, cv2.COLOR_GRAY2BGR)
    normalized_preview_bgr = cv2.cvtColor(normalized_preview, cv2.COLOR_GRAY2BGR)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_fake_12bit_raw_preview.png"), raw_preview)
    cv2.imwrite(str(output_dir / "03_normalized_preview.png"), normalized_preview)
    save_histogram(raw_uint16, normalized)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=260),
            add_label(raw_preview_bgr, "Fake 12-bit Raw", label_width=260),
            add_label(normalized_preview_bgr, "Normalized", label_width=260),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("raw min/max:", int(raw_uint16.min()), int(raw_uint16.max()))
    print("normalized min/max:", float(normalized.min()), float(normalized.max()))
    print("已保存: compare.png 和 histogram.png")


if __name__ == "__main__":
    main()
