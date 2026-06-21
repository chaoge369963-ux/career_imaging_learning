# -*- coding: utf-8 -*-
"""
第六课：给图像加高斯噪声，并计算 PSNR。

运行方式：
    python 01_opencv_basic/06_noise_and_psnr.py

本课核心函数：
    add_gaussian_noise(image_bgr, sigma)
    compute_psnr(image_a, image_b)
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
image_path = script_dir / "outputs" / "01_read_gray_hist" / "original.png"
output_dir = script_dir / "outputs" / "06_noise_and_psnr"
output_dir.mkdir(parents=True, exist_ok=True)


def add_label(image_bgr, label):
    """在图片左上角写标签，方便看对比图。"""
    labeled = image_bgr.copy()
    cv2.putText(
        labeled,
        label,
        (16, 32),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    return labeled


def add_gaussian_noise(image_bgr, sigma):
    """给 BGR 图像添加高斯噪声，返回 noisy_bgr。"""
    noise = np.random.normal(0, sigma, image_bgr.shape).astype(np.float32)
    noisy_bgr = image_bgr.astype(np.float32) + noise
    noisy_bgr = np.clip(noisy_bgr, 0, 255)
    return noisy_bgr.astype(np.uint8)


def compute_psnr(image_a, image_b):
    """计算两张同尺寸图像之间的 PSNR，返回 psnr。"""
    image_a = image_a.astype(np.float32)
    image_b = image_b.astype(np.float32)
    mse = np.mean((image_a - image_b) ** 2)

    if mse == 0:
        return float("inf")

    max_pixel = 255.0
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    return psnr


def main():
    """读取图片，添加噪声，计算 PSNR，并保存结果。"""
    image_bgr = cv2.imread(str(image_path))

    if image_bgr is None:
        raise FileNotFoundError("图片读取失败，请先运行 01_read_gray_hist.py 生成 original.png")

    print("原图 shape:", image_bgr.shape)
    print("原图 dtype:", image_bgr.dtype)

    sigma = 25
    noisy_bgr = add_gaussian_noise(image_bgr, sigma)
    psnr = compute_psnr(image_bgr, noisy_bgr)

    print("噪声图 shape:", noisy_bgr.shape)
    print("噪声图 dtype:", noisy_bgr.dtype)
    print("PSNR:", psnr)

    original_path = output_dir / "original.png"
    noisy_path = output_dir / "noisy.png"
    compare_path = output_dir / "compare.png"

    cv2.imwrite(str(original_path), image_bgr)
    cv2.imwrite(str(noisy_path), noisy_bgr)

    compare = np.hstack(
        [
            add_label(image_bgr, "Original"),
            add_label(noisy_bgr, "Noisy"),
        ]
    )
    cv2.imwrite(str(compare_path), compare)

    print("保存原图:", original_path)
    print("保存噪声图:", noisy_path)
    print("保存对比图:", compare_path)


if __name__ == "__main__":
    main()
