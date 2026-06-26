# -*- coding: utf-8 -*-
"""
传统图像复原第 6 课：去噪后再轻微锐化。

流程：
    noisy -> denoise -> denoise + unsharp mask
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

from restoration_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "06_denoise_then_sharpen_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def add_gaussian_noise(image_bgr, noise_sigma, random_seed):
    """添加高斯噪声。"""
    rng = np.random.default_rng(seed=random_seed)
    image_float = image_bgr.astype(np.float32)
    noise = rng.normal(0.0, noise_sigma, image_float.shape).astype(np.float32)
    noisy_float = image_float + noise
    noisy_float = np.clip(noisy_float, 0, 255)
    return noisy_float.astype(np.uint8)


def unsharp_mask_luminance(image_bgr, blur_size, amount):
    """
    去噪后轻微锐化。

    建议变量名：
    image_ycrcb, y, cr, cb, y_float, y_blur, y_detail, y_sharp, sharp_ycrcb, sharp_bgr
    """
    # 转到 YCrCb，只在亮度 Y 通道上做锐化，避免颜色被一起放大。
    image_ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(image_ycrcb)

    # Unsharp Mask：细节 = 原亮度 - 模糊亮度。
    y_float = y.astype(np.float32)
    y_blur = cv2.GaussianBlur(y_float, (blur_size, blur_size), 0)
    y_detail = y_float - y_blur
    y_sharp = y_float + y_detail * amount

    # 转回 uint8 前必须裁剪到 0-255，否则会出现彩色噪点/反色伪影。
    y_sharp = np.clip(y_sharp, 0, 255).astype(np.uint8)

    sharp_ycrcb = cv2.merge((y_sharp, cr, cb))
    sharp_bgr = cv2.cvtColor(sharp_ycrcb, cv2.COLOR_YCrCb2BGR)
    return sharp_bgr


def calculate_psnr(image_a, image_b):
    """计算两张 8-bit 图像之间的 PSNR。"""
    image_a = image_a.astype(np.float32)
    image_b = image_b.astype(np.float32)
    mse = np.mean((image_a - image_b) ** 2)
    if mse == 0:
        return float("inf")
    return 20 * np.log10(255.0 / np.sqrt(mse))


def main():
    """读取图片，加噪声，去噪，再轻微锐化。"""
    parser = argparse.ArgumentParser(description="Denoise then sharpen practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--noise-sigma", type=float, default=20.0, help="噪声强度")
    parser.add_argument("--kernel-size", type=int, default=5, help="高斯去噪核大小，必须是奇数")
    parser.add_argument("--blur-size", type=int, default=9, help="Unsharp Mask 模糊核大小，必须是奇数")
    parser.add_argument("--amount", type=float, default=0.8, help="轻微锐化强度")
    parser.add_argument("--seed", type=int, default=0, help="随机种子")
    args = parser.parse_args()

    if args.kernel_size % 2 == 0:
        raise ValueError("kernel-size 必须是奇数")
    if args.blur_size % 2 == 0:
        raise ValueError("blur-size 必须是奇数")

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=340)

    noisy_bgr = add_gaussian_noise(image_bgr, args.noise_sigma, args.seed)
    denoised_bgr = cv2.GaussianBlur(noisy_bgr, (args.kernel_size, args.kernel_size), sigmaX=0)
    denoise_sharpen_bgr = unsharp_mask_luminance(denoised_bgr, args.blur_size, args.amount)

    noisy_psnr = calculate_psnr(image_bgr, noisy_bgr)
    denoised_psnr = calculate_psnr(image_bgr, denoised_bgr)
    denoise_sharpen_psnr = calculate_psnr(image_bgr, denoise_sharpen_bgr)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_noisy.png"), noisy_bgr)
    cv2.imwrite(str(output_dir / "03_denoised.png"), denoised_bgr)
    cv2.imwrite(str(output_dir / "04_denoise_then_sharpen.png"), denoise_sharpen_bgr)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=220),
            add_label(noisy_bgr, "Noisy", label_width=220),
            add_label(denoised_bgr, "Denoised", label_width=240),
            add_label(denoise_sharpen_bgr, "Denoise + Sharpen", label_width=340),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("noisy PSNR:", float(noisy_psnr))
    print("denoised PSNR:", float(denoised_psnr))
    print("denoise + sharpen PSNR:", float(denoise_sharpen_psnr))
    print("已保存: compare.png")


if __name__ == "__main__":
    main()
