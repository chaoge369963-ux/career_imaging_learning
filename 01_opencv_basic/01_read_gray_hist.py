# -*- coding: utf-8 -*-
"""
第一课：读取图片、转灰度、画直方图。

运行方式：
    python 01_opencv_basic/01_read_gray_hist.py

如果你手里有自己的图片，也可以这样运行：
    python 01_opencv_basic/01_read_gray_hist.py --image path/to/your_image.jpg
"""

import argparse
from pathlib import Path

import cv2
import matplotlib
import numpy as np


# 使用 Agg 后端，脚本就可以只保存图片，不弹出窗口。
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def create_demo_image(image_path):
    """创建一张练习用彩色图，避免第一课依赖外部图片。"""
    # 图像高度 H 和宽度 W，单位是像素。
    height = 320
    width = 480

    # x 方向从黑到亮，用来构造蓝色通道。
    x = np.linspace(0, 255, width, dtype=np.uint8)
    blue = np.tile(x, (height, 1))

    # y 方向从黑到亮，用来构造绿色通道。
    y = np.linspace(0, 255, height, dtype=np.uint8).reshape(height, 1)
    green = np.tile(y, (1, width))

    # 红色通道和蓝色方向相反，让颜色变化更明显。
    red = 255 - blue

    # OpenCV 里彩色图默认是 BGR 顺序，不是 RGB 顺序。
    image_bgr = cv2.merge([blue, green, red])

    # 画一个白色圆和一个黑色矩形，方便观察灰度和直方图变化。
    cv2.circle(image_bgr, center=(120, 160), radius=55, color=(255, 255, 255), thickness=-1)
    cv2.rectangle(image_bgr, pt1=(300, 90), pt2=(420, 230), color=(0, 0, 0), thickness=-1)

    # 保存练习图。cv2.imwrite 的路径要转成字符串。
    cv2.imwrite(str(image_path), image_bgr)

    return image_bgr


def save_histogram(gray_image, output_path):
    """计算灰度直方图，并保存成曲线图。"""
    # 灰度值范围是 0 到 255，所以这里统计 256 个亮度桶。
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

    # Matplotlib 负责把直方图画成图片。
    plt.figure(figsize=(8, 4))
    plt.plot(hist, color="black")
    plt.title("Gray Histogram")
    plt.xlabel("Pixel value")
    plt.ylabel("Count")
    plt.xlim([0, 255])
    plt.tight_layout()
    plt.savefig(str(output_path), dpi=150)
    plt.close()


def main():
    """主流程：准备图片、转灰度、保存结果、打印 shape。"""
    parser = argparse.ArgumentParser(description="读取图片，保存灰度图和灰度直方图。")
    parser.add_argument("--image", type=str, default="", help="输入图片路径；不填则自动生成练习图。")
    args = parser.parse_args()

    # 当前脚本所在目录是 01_opencv_basic。
    script_dir = Path(__file__).resolve().parent

    # 本课所有输出都放在单独子目录，方便之后复盘。
    output_dir = script_dir / "outputs" / "01_read_gray_hist"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 如果没有传入图片，就自动生成一张练习图。
    if args.image:
        input_path = Path(args.image)
        image_bgr = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
    else:
        input_path = output_dir / "demo_input.png"
        image_bgr = create_demo_image(input_path)

    # 如果读取失败，通常是路径写错或图片格式不支持。
    if image_bgr is None:
        raise FileNotFoundError("图片读取失败，请检查 --image 后面的路径。")

    # 彩色图 shape 通常是 高度、宽度、通道数。
    print("彩色图 shape:", image_bgr.shape)

    # 转成灰度图后，shape 只剩 高度、宽度。
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    print("灰度图 shape:", gray_image.shape)
    print("灰度图最暗的像素值:", gray_image.min())
    print("灰度图最亮的像素值:", gray_image.max())
    # 保存原图副本、灰度图和直方图。
    original_path = output_dir / "original.png"
    gray_path = output_dir / "gray.png"
    hist_path = output_dir / "histogram.png"

    cv2.imwrite(str(original_path), image_bgr)
    cv2.imwrite(str(gray_path), gray_image)
    save_histogram(gray_image, hist_path)

    # 打印输出路径，让你知道结果在哪里。
    print("输入图片:", input_path)
    print("保存原图:", original_path)
    print("保存灰度图:", gray_path)
    print("保存直方图:", hist_path)


if __name__ == "__main__":
    main()
