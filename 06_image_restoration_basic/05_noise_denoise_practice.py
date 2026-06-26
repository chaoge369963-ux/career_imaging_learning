# -*- coding: utf-8 -*-
"""
传统图像复原第 5 课：噪声与去噪。

这一课看一个取舍：
    去噪会让噪声变少，但也可能让细节变软。
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

from restoration_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "05_noise_denoise_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def add_gaussian_noise(image_bgr, noise_sigma, random_seed):
    """
    给图像添加高斯噪声。

    建议变量名：
    rng, image_float, noise, noisy_float, noisy_bgr
    """
    rng = np.random.default_rng(seed=random_seed)
    image_float = image_bgr.astype(np.float32)
    noise = rng.normal(0.0, noise_sigma, image_float.shape).astype(np.float32)
    noisy_float = image_float + noise
    noisy_float = np.clip(noisy_float, 0, 255)
    noisy_bgr = noisy_float.astype(np.uint8)
    return noisy_bgr





def denoise_with_filters(noisy_bgr, kernel_size):
    """
    用两种滤波方法去噪。

    建议变量名：
    mean_denoised, gaussian_denoised
    """

    noisy_bgr = noisy_bgr.astype(np.float32)
    # mean_kernel = np.ones((kernel_size,kernel_size))
    # mean_kernel = mean_kernel/kernel_size**2
    # mean_denoised = cv2.filter2D(noisy_bgr,-1,mean_kernel)
    mean_denoised = cv2.blur(noisy_bgr, (kernel_size, kernel_size))
    gaussian_denoised = cv2.GaussianBlur(noisy_bgr, (kernel_size, kernel_size), sigmaX=0)
    return mean_denoised.astype(np.uint8), gaussian_denoised.astype(np.uint8)


def calculate_psnr(image_a, image_b):
    """计算两张 8-bit 图像之间的 PSNR。"""
    image_a = image_a.astype(np.float32)
    image_b = image_b.astype(np.float32)
    mse = np.mean((image_a - image_b) ** 2)
    if mse == 0:
        return float("inf")
    return 20 * np.log10(255.0 / np.sqrt(mse))


def main():
    """读取图片，加噪声，再去噪并比较 PSNR。"""
    parser = argparse.ArgumentParser(description="Noise denoise practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--noise-sigma", type=float, default=20.0, help="噪声强度")
    parser.add_argument("--kernel-size", type=int, default=5, help="滤波核大小，必须是奇数")
    parser.add_argument("--seed", type=int, default=0, help="随机种子")
    args = parser.parse_args()

    if args.kernel_size % 2 == 0:
        raise ValueError("kernel-size 必须是奇数，比如 3、5、7")

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=360)
    noisy_bgr = add_gaussian_noise(image_bgr, args.noise_sigma, args.seed)
    mean_denoised, gaussian_denoised = denoise_with_filters(noisy_bgr, args.kernel_size)

    noisy_psnr = calculate_psnr(image_bgr, noisy_bgr)
    mean_psnr = calculate_psnr(image_bgr, mean_denoised)
    gaussian_psnr = calculate_psnr(image_bgr, gaussian_denoised)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_noisy.png"), noisy_bgr)
    cv2.imwrite(str(output_dir / "03_mean_denoised.png"), mean_denoised)
    cv2.imwrite(str(output_dir / "04_gaussian_denoised.png"), gaussian_denoised)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=230),
            add_label(noisy_bgr, "Noisy", label_width=230),
            add_label(mean_denoised, "Mean Denoise", label_width=280),
            add_label(gaussian_denoised, "Gaussian Denoise", label_width=320),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("noisy PSNR:", float(noisy_psnr))
    print("mean denoise PSNR:", float(mean_psnr))
    print("gaussian denoise PSNR:", float(gaussian_psnr))
    print("已保存: compare.png")


if __name__ == "__main__":
    main()
