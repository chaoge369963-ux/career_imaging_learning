# -*- coding: utf-8 -*-
"""
mini ISP 第六课：把前面步骤串成完整 pipeline。

运行方式：
    python 02_mini_isp/06_mini_isp_pipeline.py

本课核心函数：
    run_mini_isp_pipeline(image_bgr)
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
project_dir = script_dir.parent
input_path = project_dir / "01_opencv_basic" / "outputs" / "01_read_gray_hist" / "original.png"
output_dir = script_dir / "outputs" / "06_mini_isp_pipeline"
output_dir.mkdir(parents=True, exist_ok=True)


def add_label(image_bgr, label):
    """在图片左上角写标签，方便看对比图。"""
    labeled = image_bgr.copy()
    cv2.rectangle(labeled, (0, 0), (300, 42), (255, 255, 255), thickness=-1)
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


def simulate_rggb_bayer(image_bgr):
    """BGR 彩色图 -> 单通道 RGGB Bayer RAW。"""
    height, width, _ = image_bgr.shape
    blue, green, red = cv2.split(image_bgr)

    bayer_raw = np.zeros((height, width), dtype=np.uint8)
    bayer_raw[0::2, 0::2] = red[0::2, 0::2]
    bayer_raw[0::2, 1::2] = green[0::2, 1::2]
    bayer_raw[1::2, 0::2] = green[1::2, 0::2]
    bayer_raw[1::2, 1::2] = blue[1::2, 1::2]
    return bayer_raw


def demosaic_simple(bayer_raw):
    """单通道 RGGB Bayer RAW -> 三通道 BGR 彩色图。"""
    height, width = bayer_raw.shape

    blue = np.zeros((height, width), dtype=np.float32)
    green = np.zeros((height, width), dtype=np.float32)
    red = np.zeros((height, width), dtype=np.float32)

    blue_mask = np.zeros((height, width), dtype=np.float32)
    green_mask = np.zeros((height, width), dtype=np.float32)
    red_mask = np.zeros((height, width), dtype=np.float32)

    red[0::2, 0::2] = bayer_raw[0::2, 0::2]
    red_mask[0::2, 0::2] = 1

    green[0::2, 1::2] = bayer_raw[0::2, 1::2]
    green[1::2, 0::2] = bayer_raw[1::2, 0::2]
    green_mask[0::2, 1::2] = 1
    green_mask[1::2, 0::2] = 1

    blue[1::2, 1::2] = bayer_raw[1::2, 1::2]
    blue_mask[1::2, 1::2] = 1

    def fill_missing(channel, mask):
        kernel = np.ones((3, 3), dtype=np.float32)
        value_sum = cv2.filter2D(channel, -1, kernel, borderType=cv2.BORDER_REFLECT)
        value_count = cv2.filter2D(mask, -1, kernel, borderType=cv2.BORDER_REFLECT)
        value_count = np.maximum(value_count, 1)
        averaged = value_sum / value_count
        return np.where(mask > 0, channel, averaged)

    blue = fill_missing(blue, blue_mask)
    green = fill_missing(green, green_mask)
    red = fill_missing(red, red_mask)

    demosaic_bgr = cv2.merge([blue, green, red])
    demosaic_bgr = np.clip(demosaic_bgr, 0, 255).astype(np.uint8)
    return demosaic_bgr


def apply_white_balance(image_bgr, blue_gain, green_gain, red_gain):
    """给 B/G/R 三个通道分别乘增益。"""
    image_float = image_bgr.astype(np.float32)
    blue, green, red = cv2.split(image_float)

    blue = blue * blue_gain
    green = green * green_gain
    red = red * red_gain

    balanced = cv2.merge([blue, green, red])
    balanced = np.clip(balanced, 0, 255).astype(np.uint8)
    return balanced


def apply_gamma(image_bgr, gamma):
    """Gamma correction。"""
    image_float = image_bgr.astype(np.float32) / 255.0
    corrected = image_float ** gamma
    corrected = np.clip(corrected * 255.0, 0, 255).astype(np.uint8)
    return corrected


def apply_reinhard_tone_mapping(image_float, exposure):
    """Reinhard tone mapping。输入可以是大于 1 的浮点图。"""
    x = image_float.astype(np.float32) * exposure
    mapped = x / (1.0 + x)
    mapped = np.clip(mapped * 255.0, 0, 255).astype(np.uint8)
    return mapped


def run_mini_isp_pipeline(image_bgr):
    input_bgr = image_bgr

    bayer_raw = simulate_rggb_bayer(input_bgr)
    demosaic_bgr = demosaic_simple(bayer_raw)

    white_balance = apply_white_balance(
        demosaic_bgr,
        blue_gain=0.9,
        green_gain=0.8,
        red_gain=1.2,
    )

    gamma = apply_gamma(white_balance, gamma=1.2)

    image_float = gamma.astype(np.float32) / 255.0 * 2.0
    tone_mapped = apply_reinhard_tone_mapping(image_float, exposure=1.05)

    return {
        "input_bgr": input_bgr,
        "bayer_raw": bayer_raw,
        "demosaic_bgr": demosaic_bgr,
        "white_balance": white_balance,
        "gamma": gamma,
        "tone_mapped": tone_mapped,
    }


def main():
    """读取输入图，运行 mini ISP pipeline，并保存每一步结果。"""
    image_bgr = cv2.imread(str(input_path), cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise FileNotFoundError("找不到输入图片，请先运行 01_opencv_basic/01_read_gray_hist.py")

    print("输入图 shape:", image_bgr.shape)
    print("输入图 dtype:", image_bgr.dtype)

    results = run_mini_isp_pipeline(image_bgr)


    cv2.imwrite(str(output_dir / "01_input_bgr.png"), results["input_bgr"])
    cv2.imwrite(str(output_dir / "02_bayer_raw.png"), results["bayer_raw"])
    cv2.imwrite(str(output_dir / "03_demosaic_bgr.png"), results["demosaic_bgr"])
    cv2.imwrite(str(output_dir / "04_white_balance.png"), results["white_balance"])
    cv2.imwrite(str(output_dir / "05_gamma.png"), results["gamma"])
    cv2.imwrite(str(output_dir / "06_tone_mapped.png"), results["tone_mapped"])

    bayer_preview = cv2.cvtColor(results["bayer_raw"], cv2.COLOR_GRAY2BGR)
    compare = np.hstack(
        [
            add_label(results["input_bgr"], "Input"),
            add_label(bayer_preview, "Bayer RAW"),
            add_label(results["demosaic_bgr"], "Demosaic"),
            add_label(results["white_balance"], "White Balance"),
            add_label(results["gamma"], "Gamma"),
            add_label(results["tone_mapped"], "Tone Mapping"),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输出目录:", output_dir)
    print("已保存: 01_input_bgr.png 到 06_tone_mapped.png，以及 compare.png")


if __name__ == "__main__":
    main()
