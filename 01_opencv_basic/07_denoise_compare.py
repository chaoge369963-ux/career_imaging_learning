# -*- coding: utf-8 -*-
"""
第七课：用均值滤波和高斯滤波做简单去噪，并比较 PSNR。

运行方式：
    python 01_opencv_basic/07_denoise_compare.py

本课重点：
    1. 对同一张噪声图尝试不同 kernel_size。
    2. 比较均值滤波和高斯滤波的 PSNR。
    3. 观察 kernel 太小/太大时，去噪效果和细节损失的变化。
"""

from pathlib import Path

import cv2
import matplotlib
import numpy as np


matplotlib.use("Agg")
import matplotlib.pyplot as plt


script_dir = Path(__file__).resolve().parent
original_path = script_dir / "outputs" / "06_noise_and_psnr" / "original.png"
noisy_path = script_dir / "outputs" / "06_noise_and_psnr" / "noisy.png"
output_dir = script_dir / "outputs" / "07_denoise_compare"
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


def denoise_mean(noisy_bgr, kernel_size):
    """对 noisy_bgr 做均值滤波去噪，返回 denoised_bgr。"""
    denoised_bgr = cv2.blur(noisy_bgr, kernel_size)
    return denoised_bgr


def denoise_gaussian(noisy_bgr, kernel_size):
    """对 noisy_bgr 做高斯滤波去噪，返回 denoised_bgr。"""
    denoised_bgr = cv2.GaussianBlur(noisy_bgr, kernel_size, 0)
    return denoised_bgr


def compute_psnr(image_a, image_b):
    """计算两张同尺寸图像之间的 PSNR，返回 psnr。"""
    image_a = image_a.astype(np.float32)
    image_b = image_b.astype(np.float32)
    mse = np.mean((image_a - image_b) ** 2)

    if mse == 0:
        return float("inf")

    psnr = 10 * np.log10((255.0 ** 2) / mse)
    return psnr


def save_psnr_curve(kernel_sizes, mean_psnrs, gaussian_psnrs):
    """把不同 kernel_size 的 PSNR 结果保存成曲线图。"""
    curve_path = output_dir / "psnr_curve.png"

    plt.figure(figsize=(8, 4))
    plt.plot(kernel_sizes, mean_psnrs, marker="o", label="Mean filter")
    plt.plot(kernel_sizes, gaussian_psnrs, marker="o", label="Gaussian filter")
    plt.xlabel("Kernel size")
    plt.ylabel("PSNR")
    plt.title("Denoising PSNR vs Kernel Size")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(str(curve_path), dpi=150)
    plt.close()

    return curve_path


def main():
    """读取原图和噪声图，对多个 kernel_size 做去噪实验。"""
    original_bgr = cv2.imread(str(original_path))
    noisy_bgr = cv2.imread(str(noisy_path))

    if original_bgr is None:
        raise FileNotFoundError("找不到 original.png，请先运行 06_noise_and_psnr.py")
    if noisy_bgr is None:
        raise FileNotFoundError("找不到 noisy.png，请先运行 06_noise_and_psnr.py")

    print("原图 shape:", original_bgr.shape)
    print("噪声图 shape:", noisy_bgr.shape)

    kernel_sizes = []
    mean_psnrs = []
    gaussian_psnrs = []

    for i in range(10):
        n = 2 * i + 3
        kernel_size = (n, n)

        mean_denoised = denoise_mean(noisy_bgr, kernel_size)
        gaussian_denoised = denoise_gaussian(noisy_bgr, kernel_size)

        mean_psnr = compute_psnr(original_bgr, mean_denoised)
        gaussian_psnr = compute_psnr(original_bgr, gaussian_denoised)

        kernel_sizes.append(n)
        mean_psnrs.append(mean_psnr)
        gaussian_psnrs.append(gaussian_psnr)

        print(
            f"核大小: {kernel_size}, "
            f"均值去噪 PSNR: {mean_psnr:.2f}, "
            f"高斯去噪 PSNR: {gaussian_psnr:.2f}"
        )

        cv2.imwrite(str(output_dir / f"mean_denoised_{n}.png"), mean_denoised)
        cv2.imwrite(str(output_dir / f"gaussian_denoised_{n}.png"), gaussian_denoised)

        compare = np.hstack(
            [
                add_label(original_bgr, "Original"),
                add_label(noisy_bgr, "Noisy"),
                add_label(mean_denoised, f"Mean {n}x{n}"),
                add_label(gaussian_denoised, f"Gaussian {n}x{n}"),
            ]
        )
        cv2.imwrite(str(output_dir / f"compare_{n}.png"), compare)

    best_mean_index = int(np.argmax(mean_psnrs))
    best_gaussian_index = int(np.argmax(gaussian_psnrs))
    curve_path = save_psnr_curve(kernel_sizes, mean_psnrs, gaussian_psnrs)

    print("输出目录:", output_dir)
    print(
        "均值滤波最佳:",
        f"{kernel_sizes[best_mean_index]}x{kernel_sizes[best_mean_index]}",
        f"PSNR={mean_psnrs[best_mean_index]:.2f}",
    )
    print(
        "高斯滤波最佳:",
        f"{kernel_sizes[best_gaussian_index]}x{kernel_sizes[best_gaussian_index]}",
        f"PSNR={gaussian_psnrs[best_gaussian_index]:.2f}",
    )
    print("保存 PSNR 曲线:", curve_path)


if __name__ == "__main__":
    main()
