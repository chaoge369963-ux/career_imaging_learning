# -*- coding: utf-8 -*-
"""
第二课：把彩色图拆成 B、G、R 三个通道。

运行方式：
    python 01_opencv_basic/02_bgr_channels.py

如果你手里有自己的图片，也可以这样运行：
    python 01_opencv_basic/02_bgr_channels.py --image path/to/your_image.jpg
"""

import argparse
from pathlib import Path

import cv2
import numpy as np


def create_demo_image(image_path):
    """创建一张练习用彩色图，方便观察 B、G、R 三个通道。"""
    height = 320
    width = 480

    # 生成横向变化的蓝色通道。
    x = np.linspace(0, 255, width, dtype=np.uint8)
    blue = np.tile(x, (height, 1))

    # 生成纵向变化的绿色通道。
    y = np.linspace(0, 255, height, dtype=np.uint8).reshape(height, 1)
    green = np.tile(y, (1, width))

    # 生成和蓝色相反的红色通道。
    red = 255 - blue

    # OpenCV 的彩色顺序是 BGR，所以这里按 blue、green、red 合并。
    image_bgr = cv2.merge([blue, green, red])

    cv2.circle(image_bgr, center=(120, 160), radius=55, color=(255, 255, 255), thickness=-1)
    cv2.rectangle(image_bgr, pt1=(300, 90), pt2=(420, 230), color=(0, 0, 0), thickness=-1)

    cv2.imwrite(str(image_path), image_bgr)
    return image_bgr


def load_or_create_image(input_path):
    """优先读取用户图片；没有图片时，使用第一课图片或自动生成练习图。"""
    if input_path:
        image_bgr = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
        if image_bgr is None:
            raise FileNotFoundError("图片读取失败，请检查 --image 后面的路径。")
        return image_bgr, Path(input_path)

    script_dir = Path(__file__).resolve().parent
    first_lesson_image = script_dir / "outputs" / "01_read_gray_hist" / "original.png"
    if first_lesson_image.exists():
        image_bgr = cv2.imread(str(first_lesson_image), cv2.IMREAD_COLOR)
        return image_bgr, first_lesson_image

    output_dir = script_dir / "outputs" / "02_bgr_channels"
    output_dir.mkdir(parents=True, exist_ok=True)
    demo_path = output_dir / "demo_input.png"
    image_bgr = create_demo_image(demo_path)
    return image_bgr, demo_path


def main():
    """主流程：读取彩色图，拆开 B/G/R 通道，保存结果。"""
    parser = argparse.ArgumentParser(description="拆开彩色图的 B、G、R 三个通道。")
    parser.add_argument("--image", type=str, default="", help="输入图片路径；不填则使用练习图。")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / "outputs" / "02_bgr_channels"
    output_dir.mkdir(parents=True, exist_ok=True)

    image_bgr, source_path = load_or_create_image(args.image)

    # 彩色图的 shape 是 H、W、3，最后的 3 就是 B/G/R 三个通道。
    print("输入图片:", source_path)
    print("彩色图 shape:", image_bgr.shape)
    print("彩色图 dtype:", image_bgr.dtype)

    # cv2.split 会把一张 H x W x 3 的彩色图拆成三张 H x W 的灰度图。
    blue, green, red = cv2.split(image_bgr)
    print("蓝色通道 shape:", blue.shape, "最小值:", blue.min(), "最大值:", blue.max())
    print("绿色通道 shape:", green.shape, "最小值:", green.min(), "最大值:", green.max())
    print("红色通道 shape:", red.shape, "最小值:", red.min(), "最大值:", red.max())

    # 取一个像素看看：彩色图一个像素有 3 个数字。
    sample_y = image_bgr.shape[0] // 2
    sample_x = image_bgr.shape[1] // 2
    print("中间像素 BGR 值:", image_bgr[sample_y, sample_x])
    print("中间像素的蓝色值:", blue[sample_y, sample_x])
    print("中间像素的绿色值:", green[sample_y, sample_x])
    print("中间像素的红色值:", red[sample_y, sample_x])

    # 保存原图。
    cv2.imwrite(str(output_dir / "original.png"), image_bgr)

    # 保存三个通道的灰度显示图：白的地方表示这个通道数值大。
    cv2.imwrite(str(output_dir / "blue_channel_gray.png"), blue)
    cv2.imwrite(str(output_dir / "green_channel_gray.png"), green)
    cv2.imwrite(str(output_dir / "red_channel_gray.png"), red)

    # 为了直观看颜色，把另外两个通道清零，只保留一个颜色通道。
    zeros = np.zeros_like(blue)
    blue_only = cv2.merge([blue, zeros, zeros])
    green_only = cv2.merge([zeros, green, zeros])
    red_only = cv2.merge([zeros, zeros, red])

    cv2.imwrite(str(output_dir / "blue_only.png"), blue_only)
    cv2.imwrite(str(output_dir / "green_only.png"), green_only)
    cv2.imwrite(str(output_dir / "red_only.png"), red_only)

    print("输出目录:", output_dir)
    print("已保存: original.png")
    print("已保存: blue_channel_gray.png, green_channel_gray.png, red_channel_gray.png")
    print("已保存: blue_only.png, green_only.png, red_only.png")


if __name__ == "__main__":
    main()
