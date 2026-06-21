# -*- coding: utf-8 -*-
"""
第八课：把前面几节课的结果拼成一张总览图。

运行方式：
    python 01_opencv_basic/08_before_after_grid.py

本课你要补两个核心函数：
    read_and_resize(image_path, size)
    make_grid(images, rows, cols)
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
outputs_dir = script_dir / "outputs"
output_dir = outputs_dir / "08_before_after_grid"
output_dir.mkdir(parents=True, exist_ok=True)


image_items = [
    ("Original", outputs_dir / "01_read_gray_hist" / "original.png"),
    ("Gray", outputs_dir / "03_gray_hist_by_hand" / "gray.png"),
    ("Mean Blur", outputs_dir / "04_blur_compare" / "mean_blur.png"),
    ("Sharpen", outputs_dir / "05_sharpen_kernel" / "sharpened.png"),
    ("Noisy", outputs_dir / "06_noise_and_psnr" / "noisy.png"),
    ("Denoised", outputs_dir / "07_denoise_compare" / "gaussian_denoised_7.png"),
    ("PSNR Curve", outputs_dir / "07_denoise_compare" / "psnr_curve.png"),
]


def add_label(image_bgr, label):
    """在图片左上角写标签，方便看总览图。"""
    labeled = image_bgr.copy()
    cv2.rectangle(labeled, (0, 0), (220, 42), (255, 255, 255), thickness=-1)
    cv2.putText(
        labeled,
        label,
        (12, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    return labeled


def read_and_resize(image_path, size):
    """读取一张图片，转换成 BGR 三通道，缩放到指定 size。"""
    image_bgr = cv2.imread(image_path)

    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败.image_path")
    if image_bgr.shape == 2:
        image_bgr = cv2.cvtColor(image_bgr,cv2.COLOR_GRAY2BGR)
    image_bgr = cv2.resize(image_bgr,size)
    return  image_bgr

def make_grid(images, rows, cols):
    """把多张同尺寸图片按 rows x cols 拼成一张大图。"""
    row_images = []
    for r in range(rows):
        row_image = np.hstack(images[r*cols:(r+1)*cols])
        row_images.append(row_image)
    big_image = np.vstack(row_images)
    return big_image
    raise NotImplementedError("请补完 make_grid(images, rows, cols)")


def main():
    """读取前面课程的结果图，并保存总览图。"""
    tile_size = (360, 240)  # 宽、高
    rows = 2
    cols = 4

    images = []
    for label, path in image_items:
        image_bgr = read_and_resize(path, tile_size)
        image_bgr = add_label(image_bgr, label)
        images.append(image_bgr)
        print("读取:", path)

    # 现在有 7 张图，补一张空白图，让它变成 2 x 4。
    blank = np.full((tile_size[1], tile_size[0], 3), 255, dtype=np.uint8)
    blank = add_label(blank, "Summary")
    images.append(blank)

    grid = make_grid(images, rows, cols)
    grid_path = output_dir / "opencv_basic_summary.png"
    cv2.imwrite(str(grid_path), grid)

    print("保存总览图:", grid_path)


if __name__ == "__main__":
    main()
