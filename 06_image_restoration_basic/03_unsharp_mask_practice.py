# -*- coding: utf-8 -*-
"""
传统图像复原第 3 课：Unsharp Mask 反差保留锐化。

核心思想：
    1. 先把图像模糊，得到低频图
    2. 原图 - 模糊图，得到高频细节
    3. 原图 + amount * 高频细节，得到锐化图

这比直接套锐化核更常见，也更容易控制锐化强度。
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

from restoration_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "03_unsharp_mask_practice"
output_dir.mkdir(parents=True, exist_ok=True)


def unsharp_mask_luminance(image_bgr, blur_size, amount):
    """
    功能：
    只在亮度通道上做 Unsharp Mask。

    你要完成的步骤：

    """
    image_ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(image_ycrcb)
    y_float = y.astype(np.float32)
    y_blur = cv2.GaussianBlur(y_float, (blur_size, blur_size), 0)
    y_detail = y_float - y_blur
    y_sharpened = y_float + amount * y_detail
    y_sharpened = np.clip(y_sharpened, 0, 255).astype(np.uint8)

    sharp_ycrcb = cv2.merge((y_sharpened, cr, cb))
    return cv2.cvtColor(sharp_ycrcb, cv2.COLOR_YCrCb2BGR)


def make_detail_preview(image_bgr, blur_size):
    """生成细节层预览图：原亮度 - 模糊亮度，再平移到可显示范围。"""
    image_ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    y, _, _ = cv2.split(image_ycrcb)
    y_float = y.astype(np.float32)
    y_blur = cv2.GaussianBlur(y_float, (blur_size, blur_size), 0)
    detail = y_float - y_blur

    detail_preview = np.clip(detail + 128.0, 0, 255).astype(np.uint8)
    return cv2.cvtColor(detail_preview, cv2.COLOR_GRAY2BGR)


def main():
    """读取图片，执行 Unsharp Mask，并保存对比图。"""
    parser = argparse.ArgumentParser(description="Unsharp mask practice")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--blur-size", type=int, default=9, help="高斯模糊核大小，必须是奇数")
    parser.add_argument("--amount", type=float, default=1.2, help="锐化强度")
    args = parser.parse_args()

    if args.blur_size % 2 == 0:
        raise ValueError("blur-size 必须是奇数，比如 5、7、9")

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    image_bgr = resize_for_demo(image_bgr, max_width=380)
    detail_preview = make_detail_preview(image_bgr, args.blur_size)
    sharpened = unsharp_mask_luminance(image_bgr, args.blur_size, args.amount)

    cv2.imwrite(str(output_dir / "01_input.png"), image_bgr)
    cv2.imwrite(str(output_dir / "02_detail_layer.png"), detail_preview)
    cv2.imwrite(str(output_dir / "03_unsharp_mask.png"), sharpened)

    compare = np.hstack(
        [
            add_label(image_bgr, "Input", label_width=240),
            add_label(detail_preview, "Detail Layer", label_width=280),
            add_label(sharpened, "Unsharp Mask", label_width=300),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("blur size:", args.blur_size)
    print("amount:", args.amount)
    print("已保存: compare.png")


if __name__ == "__main__":
    main()
