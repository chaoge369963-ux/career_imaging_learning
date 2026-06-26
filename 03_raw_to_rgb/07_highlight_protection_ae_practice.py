# -*- coding: utf-8 -*-
"""
高光保护自动曝光练习。

上一节的自动曝光只看平均亮度：
    gain = target_mean / current_mean

这一节加一个约束：
    过曝比例 clipped_ratio 不能超过 max_clipped_ratio

这就更接近真实相机里的自动曝光：不能只追求整体变亮，还要保护高光。
"""

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from raw_to_rgb_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "07_highlight_protection_ae_practice"
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


def calculate_clipped_ratio(image_float):
    """
    任务 1：
    计算过曝比例。

    提示：
    - image_float >= 1.0 会得到 True/False 数组
    - np.mean(True/False) 就是 True 的比例
    """
    return np.mean(image_float >= 1.0)
 

def calculate_mean_based_gain(normalized_raw, target_mean, max_gain):
    """
    任务 2：
    根据平均亮度计算一个基础 gain。

    提示：
    - current_mean = normalized_raw.mean()
    - gain = target_mean / max(current_mean, 1e-6)
    - gain 限制在 1.0 到 max_gain
    """
    current_mean = normalized_raw.mean()
    gain = target_mean / max(current_mean, 1e-6)
    gain = np.clip(gain, 1.0, max_gain)
    return gain

def find_highlight_safe_gain(normalized_raw, desired_gain, max_clipped_ratio, search_steps):
    """
    任务 3：
    用二分搜索找到一个更安全的 gain。

    目标：
    - gain 尽量接近 desired_gain
    - 但 apply_exposure_gain 后的 clipped_ratio 不能超过 max_clipped_ratio

    提示：
    1. low = 1.0
    2. high = desired_gain
    3. 重复 search_steps 次：
       - mid = (low + high) / 2
       - test_raw = apply_exposure_gain(normalized_raw, mid)
       - clipped_ratio = calculate_clipped_ratio(test_raw)
       - 如果 clipped_ratio <= max_clipped_ratio，说明 mid 还安全，low = mid
       - 否则 mid 太亮了，high = mid
    4. 返回 low
    """
    low = 1.0
    high = desired_gain
    for i in range(search_steps):
        mid = (low + high) / 2
        test_raw = apply_exposure_gain(normalized_raw, mid)
        clipped_ration = calculate_clipped_ratio(test_raw)
        if clipped_ration <= max_clipped_ratio:
            low = mid
        else:
            high = mid
        i += 1
    return low
    


def to_preview_bgr(image_float):
    """把 0.0 到 1.0 的单通道图转成 BGR 预览图。"""
    image_uint8 = (image_float * 255.0).astype(np.uint8)
    return cv2.cvtColor(image_uint8, cv2.COLOR_GRAY2BGR)


def save_histogram(before, mean_only, highlight_safe):
    """保存三种亮度分布的直方图。"""
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.hist(before.ravel(), bins=80, range=(0.0, 1.0))
    plt.title("Before")
    plt.xlabel("value")
    plt.ylabel("count")

    plt.subplot(1, 3, 2)
    plt.hist(mean_only.ravel(), bins=80, range=(0.0, 1.0))
    plt.title("Mean AE")
    plt.xlabel("value")

    plt.subplot(1, 3, 3)
    plt.hist(highlight_safe.ravel(), bins=80, range=(0.0, 1.0))
    plt.title("Highlight-safe AE")
    plt.xlabel("value")

    plt.tight_layout()
    plt.savefig(output_dir / "histogram.png", dpi=150)
    plt.close()


def main():
    """读取图片，比较普通自动曝光和高光保护自动曝光。"""
    parser = argparse.ArgumentParser(description="Highlight protection auto exposure practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--target-mean", type=float, default=0.80, help="目标平均亮度")
    parser.add_argument("--max-gain", type=float, default=4.0, help="最大曝光增益")
    parser.add_argument("--max-clipped-ratio", type=float, default=0.05, help="允许的最大过曝比例")
    parser.add_argument("--search-steps", type=int, default=20, help="二分搜索次数")
    args = parser.parse_args()

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=360)
    normalized_raw = simulate_normalized_raw(image_bgr)

    mean_gain = calculate_mean_based_gain(normalized_raw, args.target_mean, args.max_gain)
    mean_raw = apply_exposure_gain(normalized_raw, mean_gain)

    safe_gain = find_highlight_safe_gain(
        normalized_raw,
        desired_gain=mean_gain,
        max_clipped_ratio=args.max_clipped_ratio,
        search_steps=args.search_steps,
    )
    safe_raw = apply_exposure_gain(normalized_raw, safe_gain)

    mean_clipped_ratio = calculate_clipped_ratio(mean_raw)
    safe_clipped_ratio = calculate_clipped_ratio(safe_raw)

    before_bgr = to_preview_bgr(normalized_raw)
    mean_bgr = to_preview_bgr(mean_raw)
    safe_bgr = to_preview_bgr(safe_raw)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_before_exposure.png"), before_bgr)
    cv2.imwrite(str(output_dir / "03_mean_auto_exposure.png"), mean_bgr)
    cv2.imwrite(str(output_dir / "04_highlight_safe_exposure.png"), safe_bgr)
    save_histogram(normalized_raw, mean_raw, safe_raw)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=240),
            add_label(before_bgr, "Before", label_width=240),
            add_label(mean_bgr, "Mean AE", label_width=240),
            add_label(safe_bgr, "Highlight-safe AE", label_width=320),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("raw mean:", float(normalized_raw.mean()))
    print("target mean:", float(args.target_mean))
    print("mean gain:", float(mean_gain))
    print("mean clipped ratio:", float(mean_clipped_ratio))
    print("safe gain:", float(safe_gain))
    print("safe clipped ratio:", float(safe_clipped_ratio))
    print("已保存: compare.png 和 histogram.png")


if __name__ == "__main__":
    main()
