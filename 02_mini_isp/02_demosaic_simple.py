# -*- coding: utf-8 -*-
"""
mini ISP 第二课：把 RGGB Bayer RAW 简单恢复成 BGR 彩色图。

运行方式：
    python 02_mini_isp/02_demosaic_simple.py

本课核心函数：
    demosaic_simple(bayer_raw)
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
input_dir = script_dir / "outputs" / "01_fake_bayer"
output_dir = script_dir / "outputs" / "02_demosaic_simple"
output_dir.mkdir(parents=True, exist_ok=True)

bayer_path = input_dir / "fake_bayer_raw.png"
reference_path = input_dir / "input_bgr.png"


def add_label(image_bgr, label):
    """在图片左上角写标签，方便看对比图。"""
    labeled = image_bgr.copy()
    cv2.rectangle(labeled, (0, 0), (230, 42), (255, 255, 255), thickness=-1)
    cv2.putText(
        labeled,
        label,
        (12, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )
    return labeled


def demosaic_simple(bayer_raw):
    """把单通道 RGGB Bayer RAW 恢复成三通道 BGR 彩色图。"""
    x, y = bayer_raw.shape

    blue = np.zeros((x, y), dtype=np.float32)
    blue_mask = np.zeros((x, y), dtype=np.float32)
    green = np.zeros((x, y), dtype=np.float32)
    green_mask = np.zeros((x, y), dtype=np.float32)
    red = np.zeros((x, y), dtype=np.float32)
    red_mask = np.zeros((x, y), dtype=np.float32)

    blue[1::2, 1::2] = bayer_raw[1::2, 1::2]
    blue_mask[1::2, 1::2]= 1

    green[0::2, 1::2] = bayer_raw[0::2, 1::2]
    green[1::2, 0::2] = bayer_raw[1::2, 0::2]
    green_mask[0::2, 1::2] = 1
    green_mask[1::2, 0::2] = 1

    red[0::2, 0::2] = bayer_raw[0::2, 0::2]
    red_mask[0::2, 0::2] = 1

    def fill_missing(channel, mask):
        kernel = np.ones((3, 3), dtype=np.float32)
        value_sum = cv2.filter2D(channel, -1, kernel, borderType=cv2.BORDER_REFLECT)
        value_count = cv2.filter2D(mask, -1, kernel, borderType=cv2.BORDER_REFLECT)
        value_count = np.maximum(value_count, 1)
        averaged = value_sum / value_count
        filled = np.where(mask > 0, channel, averaged)
        return filled

    red = fill_missing(red, red_mask)
    blue = fill_missing(blue, blue_mask)
    green = fill_missing(green, green_mask)

    demosaic_bgr = cv2.merge([blue, green, red])
    demosaic_bgr = np.clip(demosaic_bgr, 0, 255).astype(np.uint8)
    return demosaic_bgr   


def main():
    """读取 Bayer RAW，做简单 demosaic，并保存结果。"""
    bayer_raw = cv2.imread(str(bayer_path), cv2.IMREAD_GRAYSCALE)
    reference_bgr = cv2.imread(str(reference_path), cv2.IMREAD_COLOR)

    if bayer_raw is None:
        raise FileNotFoundError("找不到 fake_bayer_raw.png，请先运行 02_mini_isp/01_fake_bayer.py")
    if reference_bgr is None:
        raise FileNotFoundError("找不到 input_bgr.png，请先运行 02_mini_isp/01_fake_bayer.py")

    print("Bayer RAW shape:", bayer_raw.shape)
    print("Bayer RAW dtype:", bayer_raw.dtype)

    demosaic_bgr = demosaic_simple(bayer_raw)

    print("Demosaic BGR shape:", demosaic_bgr.shape)
    print("Demosaic BGR dtype:", demosaic_bgr.dtype)

    bayer_preview = cv2.cvtColor(bayer_raw, cv2.COLOR_GRAY2BGR)
    compare = np.hstack(
        [
            add_label(reference_bgr, "Reference BGR"),
            add_label(bayer_preview, "Bayer RAW"),
            add_label(demosaic_bgr, "Demosaic BGR"),
        ]
    )

    cv2.imwrite(str(output_dir / "bayer_raw.png"), bayer_raw)
    cv2.imwrite(str(output_dir / "demosaic_bgr.png"), demosaic_bgr)
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输出目录:", output_dir)
    print("已保存: bayer_raw.png, demosaic_bgr.png, compare.png")


if __name__ == "__main__":
    main()
