# -*- coding: utf-8 -*-
"""
自动曝光 Auto Exposure 挑战练习。

上一节是手动给 gain：
    output = raw * gain

这一节升级为：
    程序根据图像亮度，自动算 gain，
    同时检查有多少像素被裁剪到 1.0。
"""

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from raw_to_rgb_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "06_auto_exposure_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def simulate_normalized_raw(image_bgr):
    """用灰度图模拟已经归一化到 0.0 到 1.0 的线性 RAW。"""
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    normalized_raw = image_gray.astype(np.float32) / 255.0
    return normalized_raw


def apply_exposure_gain(normalized_raw, gain):
    """曝光补偿：乘 gain，然后限制到 0.0 到 1.0。"""
    exposure_raw = normalized_raw * gain
    return np.clip(exposure_raw, 0.0, 1.0)


def calculate_auto_gain(normalized_raw, target_mean, max_gain):
    """
    挑战 1：
    根据当前平均亮度，自动计算 gain。

    思路：
    - current_mean = normalized_raw.mean()
    - 如果 current_mean 很小，直接除会危险，所以要用 max(current_mean, 1e-6)
    - gain = target_mean / current_mean
    - gain 不能无限大，要限制在 1.0 到 max_gain

    返回：
    - gain，一个 float 数字
    """
    current_mean = normalized_raw.mean()
    current_mean = max(current_mean,1e-6)
    gain = target_mean/current_mean
    gain = np.clip(gain,1.0,max_gain)
    return gain

def calculate_clipped_ratio(image_float):
    """
    挑战 2：
    计算过曝比例。

    思路：
    - image_float >= 1.0 会得到 True/False 数组
    - np.mean(True/False) 可以得到 True 的比例

    返回：
    - clipped_ratio，一个 float 数字
    """
    TF = np.where(image_float >= 1.0 ,True,False)
    x = np.mean(TF)
    return x



def to_preview_bgr(image_float):
    """把 0.0 到 1.0 的单通道图转成 BGR 预览图。"""
    image_uint8 = (image_float * 255.0).astype(np.uint8)
    return cv2.cvtColor(image_uint8, cv2.COLOR_GRAY2BGR)


def save_histogram(before, manual_after, auto_after):
    """保存自动曝光前后的直方图。"""
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.hist(before.ravel(), bins=80, range=(0.0, 1.0))
    plt.title("Before")
    plt.xlabel("value")
    plt.ylabel("count")

    plt.subplot(1, 3, 2)
    plt.hist(manual_after.ravel(), bins=80, range=(0.0, 1.0))
    plt.title("Manual Gain")
    plt.xlabel("value")

    plt.subplot(1, 3, 3)
    plt.hist(auto_after.ravel(), bins=80, range=(0.0, 1.0))
    plt.title("Auto Gain")
    plt.xlabel("value")

    plt.tight_layout()
    plt.savefig(output_dir / "histogram.png", dpi=150)
    plt.close()


def main():
    """读取图片，比较手动曝光和自动曝光。"""
    parser = argparse.ArgumentParser(description="Auto exposure practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--manual-gain", type=float, default=2.5, help="手动曝光增益")
    parser.add_argument("--target-mean", type=float, default=0.55, help="自动曝光目标平均亮度")
    parser.add_argument("--max-gain", type=float, default=4.0, help="自动曝光最大增益")
    args = parser.parse_args()

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=380)
    normalized_raw = simulate_normalized_raw(image_bgr)

    manual_raw = apply_exposure_gain(normalized_raw, args.manual_gain)
    auto_gain = calculate_auto_gain(normalized_raw, args.target_mean, args.max_gain)
    auto_raw = apply_exposure_gain(normalized_raw, auto_gain)

    manual_clipped_ratio = calculate_clipped_ratio(manual_raw)
    auto_clipped_ratio = calculate_clipped_ratio(auto_raw)

    before_bgr = to_preview_bgr(normalized_raw)
    manual_bgr = to_preview_bgr(manual_raw)
    auto_bgr = to_preview_bgr(auto_raw)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_before_exposure.png"), before_bgr)
    cv2.imwrite(str(output_dir / "03_manual_exposure.png"), manual_bgr)
    cv2.imwrite(str(output_dir / "04_auto_exposure.png"), auto_bgr)
    save_histogram(normalized_raw, manual_raw, auto_raw)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=250),
            add_label(before_bgr, "Before", label_width=250),
            add_label(manual_bgr, "Manual Gain", label_width=250),
            add_label(auto_bgr, "Auto Gain", label_width=250),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("raw mean:", float(normalized_raw.mean()))
    print("manual gain:", float(args.manual_gain))
    print("manual clipped ratio:", float(manual_clipped_ratio))
    print("auto gain:", float(auto_gain))
    print("auto clipped ratio:", float(auto_clipped_ratio))
    print("已保存: compare.png 和 histogram.png")


if __name__ == "__main__":
    main()
