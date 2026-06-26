# -*- coding: utf-8 -*-
"""
传统图像复原第 4 课：运动模糊与简单恢复。

这一课的重点：
    图像退化 = 清晰图经过一个模糊 kernel 变坏
    简单锐化 = 让图看起来更清楚，但不一定真的恢复原始细节
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

from restoration_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "04_motion_blur_restore_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def make_horizontal_motion_kernel(kernel_size):
    """
    功能：
    创建一个水平运动模糊 kernel。

    例子：
    kernel_size = 5 时，中间一行全是 1/5，其他位置是 0。

    你要完成的步骤：
  
    """
    A = np.zeros((kernel_size,kernel_size))
    a = kernel_size // 2 
    A[a,:] = 1/kernel_size
    return A

def apply_kernel(image_bgr, kernel):
    """使用 filter2D 应用卷积核。"""
    return cv2.filter2D(image_bgr, -1, kernel, borderType=cv2.BORDER_REFLECT)


def unsharp_mask_luminance(image_bgr, blur_size, amount):
    """只在亮度通道上做 Unsharp Mask，用作简单恢复尝试。"""
    image_ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(image_ycrcb)

    y_float = y.astype(np.float32)
    y_blur = cv2.GaussianBlur(y_float, (blur_size, blur_size), 0)
    detail = y_float - y_blur
    y_sharp = y_float + amount * detail
    y_sharp = np.clip(y_sharp, 0, 255).astype(np.uint8)

    sharp_ycrcb = cv2.merge((y_sharp, cr, cb))
    return cv2.cvtColor(sharp_ycrcb, cv2.COLOR_YCrCb2BGR)


def calculate_psnr(image_a, image_b):
    """
    功能：
    计算两张 8-bit 图像之间的 PSNR。


    """
    image_a = image_a.astype(np.float32)
    image_b = image_b.astype(np.float32)
    mse = np.mean((image_a - image_b)**2)
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr



def print_kernel(name, kernel):
    """打印 kernel，观察形状和数值和。"""
    print(name)
    print(kernel)
    print("shape:", kernel.shape, "sum:", float(kernel.sum()))


def main():
    """读取图片，制造运动模糊，再尝试用 Unsharp Mask 恢复。"""
    parser = argparse.ArgumentParser(description="Motion blur restore practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--motion-size", type=int, default=15, help="运动模糊长度，建议奇数")
    parser.add_argument("--amount", type=float, default=1.6, help="Unsharp Mask 锐化强度")
    parser.add_argument("--blur-size", type=int, default=9, help="Unsharp Mask 的高斯模糊核大小")
    args = parser.parse_args()

    if args.motion_size % 2 == 0:
        raise ValueError("motion-size 建议用奇数，比如 9、15、21")
    if args.blur_size % 2 == 0:
        raise ValueError("blur-size 必须是奇数，比如 5、9、15")

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=380)
    motion_kernel = make_horizontal_motion_kernel(args.motion_size)
    print_kernel("motion blur kernel", motion_kernel)

    motion_blur = apply_kernel(image_bgr, motion_kernel)
    restored = unsharp_mask_luminance(motion_blur, args.blur_size, args.amount)

    blur_psnr = calculate_psnr(image_bgr, motion_blur)
    restored_psnr = calculate_psnr(image_bgr, restored)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_motion_blur.png"), motion_blur)
    cv2.imwrite(str(output_dir / "03_unsharp_restore.png"), restored)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=240),
            add_label(motion_blur, "Motion Blur", label_width=280),
            add_label(restored, "Unsharp Restore", label_width=320),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("motion blur PSNR:", float(blur_psnr))
    print("unsharp restore PSNR:", float(restored_psnr))
    print("已保存: compare.png")


if __name__ == "__main__":
    main()
