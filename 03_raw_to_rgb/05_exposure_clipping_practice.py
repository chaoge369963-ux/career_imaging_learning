# -*- coding: utf-8 -*-
"""
曝光补偿 / 裁剪练习。

这一节观察一个现象：
    归一化后的 RAW 乘 exposure_gain 会变亮，
    但超过 1.0 的部分会被裁剪，形成过曝。
"""

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from raw_to_rgb_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "05_exposure_clipping_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def simulate_normalized_raw(image_bgr):
    """用灰度图模拟已经归一化到 0.0 到 1.0 的线性 RAW。"""
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    normalized_raw = image_gray.astype(np.float32) / 255.0
    return normalized_raw


def apply_exposure_gain(normalized_raw, exposure_gain):
    """
    功能：
    对归一化 RAW 做曝光补偿。

    你要完成的步骤：
    1. normalized_raw 乘 exposure_gain
    2. 用 np.clip 限制到 0.0 到 1.0
    3. 返回结果
    """
    gain_bgr = normalized_raw * exposure_gain
    gain_bgr = np.clip(gain_bgr,0.0,1.0)
    return gain_bgr



def to_preview_bgr(image_float):
    """把 0.0 到 1.0 的单通道图转成可保存的 BGR 预览图。"""
    image_uint8 = (image_float * 255.0).astype(np.uint8)
    return cv2.cvtColor(image_uint8, cv2.COLOR_GRAY2BGR)


def save_histogram(before, after):
    """保存曝光补偿前后的直方图。"""
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.hist(before.ravel(), bins=80, range=(0.0, 1.0))
    plt.title("Before exposure")
    plt.xlabel("value")
    plt.ylabel("count")

    plt.subplot(1, 2, 2)
    plt.hist(after.ravel(), bins=80, range=(0.0, 1.0))
    plt.title("After exposure")
    plt.xlabel("value")
    plt.ylabel("count")

    plt.tight_layout()
    plt.savefig(output_dir / "histogram.png", dpi=150)
    plt.close()


def main():
    """读取图片，模拟线性 RAW，调用你的曝光补偿函数。"""
    parser = argparse.ArgumentParser(description="Exposure clipping practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--gain", type=float, default=1.8, help="曝光补偿系数")
    args = parser.parse_args()

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=420)
    normalized_raw = simulate_normalized_raw(image_bgr)
    exposure_raw = apply_exposure_gain(normalized_raw, args.gain)

    before_bgr = to_preview_bgr(normalized_raw)
    after_bgr = to_preview_bgr(exposure_raw)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_before_exposure.png"), before_bgr)
    cv2.imwrite(str(output_dir / "03_after_exposure.png"), after_bgr)
    save_histogram(normalized_raw, exposure_raw)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=260),
            add_label(before_bgr, "Before Gain", label_width=260),
            add_label(after_bgr, "After Gain", label_width=260),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    clipped_ratio = np.mean(exposure_raw >= 1.0)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("gain:", args.gain)
    print("before min/max:", float(normalized_raw.min()), float(normalized_raw.max()))
    print("after min/max:", float(exposure_raw.min()), float(exposure_raw.max()))
    print("clipped ratio:", float(clipped_ratio))
    print("已保存: compare.png 和 histogram.png")


if __name__ == "__main__":
    main()
