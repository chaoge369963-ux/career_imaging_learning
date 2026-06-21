# -*- coding: utf-8 -*-
"""
mini ISP 第一课：从彩色图模拟 RGGB Bayer RAW。

运行方式：
    python 02_mini_isp/01_fake_bayer.py

本课核心函数：
    simulate_rggb_bayer(image_bgr)
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
project_dir = script_dir.parent
image_path = project_dir / "01_opencv_basic" / "outputs" / "01_read_gray_hist" / "original.png"
output_dir = script_dir / "outputs" / "01_fake_bayer"
output_dir.mkdir(parents=True, exist_ok=True)


def create_demo_image(image_path):
    """如果找不到 OpenCV 第一课图片，就自动生成一张练习图。"""
    height = 320
    width = 480

    x = np.linspace(0, 255, width, dtype=np.uint8)
    blue = np.tile(x, (height, 1))

    y = np.linspace(0, 255, height, dtype=np.uint8).reshape(height, 1)
    green = np.tile(y, (1, width))

    red = 255 - blue

    image_bgr = cv2.merge([blue, green, red])
    cv2.circle(image_bgr, center=(120, 160), radius=55, color=(255, 255, 255), thickness=-1)
    cv2.rectangle(image_bgr, pt1=(300, 90), pt2=(420, 230), color=(0, 0, 0), thickness=-1)
    cv2.imwrite(str(image_path), image_bgr)
    return image_bgr


def load_input_image():
    """读取输入图；如果不存在，就生成一张练习图。"""
    image_bgr = cv2.imread(str(image_path))

    if image_bgr is not None:
        return image_bgr

    demo_path = output_dir / "demo_input.png"
    return create_demo_image(demo_path)


def simulate_rggb_bayer(image_bgr):
    """把 BGR 彩色图模拟成单通道 RGGB Bayer 图。"""
    x,y,z = image_bgr.shape
    image_blue,image_green,image_red =cv2.split(image_bgr)


    image_rggb = np.zeros((x,y), dtype=np.uint8)
    # for i in range(x):
        
    #     for j in range(y):
         
    #         if i%2==0 and j%2==0:
    #             image_rggb[i,j] = image_red[i,j]
    #         elif i%2==0 and j%2==1:
    #             image_rggb[i,j] = image_green[i,j]
    #         elif i%2==1 and j%2==0:
    #             image_rggb[i,j] = image_green[i,j]
    #         elif i%2==1 and j%2==1:
    #             image_rggb[i,j-1] = image_blue[i,j]
    #         j = j + 1
    #     i = i+1
    # return image_rggb
    image_rggb[0::2,0::2] = image_red[0::2,0::2]
    image_rggb[1::2,0::2] = image_green[1::2,0::2]
    image_rggb[0::2,1::2] = image_green[0::2,1::2]
    image_rggb[1::2,1::2] = image_blue[1::2,1::2]
    return image_rggb


    raise NotImplementedError("请补完 simulate_rggb_bayer(image_bgr)")


def make_bayer_preview(bayer_raw):
    """把单通道 Bayer 图放大显示，方便肉眼查看采样格子。"""
    preview = cv2.normalize(bayer_raw, None, 0, 255, cv2.NORM_MINMAX)
    preview = preview.astype(np.uint8)
    return preview


def main():
    """读取彩色图，模拟 Bayer RAW，并保存结果。"""
    image_bgr = load_input_image()

    print("输入彩色图 shape:", image_bgr.shape)
    print("输入彩色图 dtype:", image_bgr.dtype)

    bayer_raw = simulate_rggb_bayer(image_bgr)

    print("Bayer RAW shape:", bayer_raw.shape)
    print("Bayer RAW dtype:", bayer_raw.dtype)
    print("Bayer RAW 最小值:", bayer_raw.min())
    print("Bayer RAW 最大值:", bayer_raw.max())

    bayer_preview = make_bayer_preview(bayer_raw)

    cv2.imwrite(str(output_dir / "input_bgr.png"), image_bgr)
    cv2.imwrite(str(output_dir / "fake_bayer_raw.png"), bayer_raw)
    cv2.imwrite(str(output_dir / "fake_bayer_preview.png"), bayer_preview)

    print("输出目录:", output_dir)
    print("已保存: input_bgr.png, fake_bayer_raw.png, fake_bayer_preview.png")


if __name__ == "__main__":
    main()
