# -*- coding: utf-8 -*-
"""
RAW-to-RGB demo：把一张 BGR 图模拟成 Bayer RAW，再恢复成可显示图像。

运行方式：
    python 03_raw_to_rgb/01_raw_to_rgb_demo.py

使用自己的图片：
    python 03_raw_to_rgb/01_raw_to_rgb_demo.py --image C:/path/to/image.png
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

from raw_to_rgb_utils import add_label, get_default_image_path, read_image_bgr, resize_for_demo


script_dir = Path(__file__).resolve().parent
default_image_path = get_default_image_path()
output_dir = script_dir / "outputs" / "01_raw_to_rgb_demo"
output_dir.mkdir(parents=True, exist_ok=True)


def blur_before_bayer(image_bgr, blur_size):
    """在 Bayer 抽样前做轻微模糊，减少细线位置的彩色伪影。"""
    if blur_size <= 1:
        return image_bgr

    if blur_size % 2 == 0:
        blur_size = blur_size + 1

    return cv2.GaussianBlur(image_bgr, (blur_size, blur_size), 0)


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
    return np.clip(demosaic_bgr, 0, 255).astype(np.uint8)


def demosaic_opencv(bayer_raw):
    """用 OpenCV 的 demosaic API 恢复彩色图，颜色通常比手写平均法更稳。"""
    return cv2.cvtColor(bayer_raw, cv2.COLOR_BayerBG2BGR)


def apply_white_balance(image_bgr, blue_gain, green_gain, red_gain):
    """给 B/G/R 三个通道分别乘增益。"""
    image_float = image_bgr.astype(np.float32)
    blue, green, red = cv2.split(image_float)
    balanced = cv2.merge(
        [
            blue * blue_gain,
            green * green_gain,
            red * red_gain,
        ]
    )
    return np.clip(balanced, 0, 255).astype(np.uint8)


def get_color_matrix(style):
    """根据风格名字返回 3x3 颜色校正矩阵。"""
    if style == "warm":
        return np.array(
            [
                [0.95, 0.00, 0.00],
                [0.00, 1.00, 0.00],
                [0.00, 0.04, 1.08],
            ],
            dtype=np.float32,
        )

    if style == "cool":
        return np.array(
            [
                [1.12, 0.03, 0.00],
                [0.00, 1.00, 0.00],
                [0.00, 0.00, 0.92],
            ],
            dtype=np.float32,
        )

    if style == "vivid":
        return np.array(
            [
                [1.08, -0.04, -0.02],
                [-0.03, 1.08, -0.03],
                [-0.02, -0.04, 1.10],
            ],
            dtype=np.float32,
        )

    return np.array(
        [
            [1.00, 0.00, 0.00],
            [0.00, 1.00, 0.00],
            [0.00, 0.00, 1.00],
        ],
        dtype=np.float32,
    )


def apply_color_matrix(image_bgr, matrix):
    """用 3x3 颜色矩阵重新混合 B/G/R 三个通道。"""
    image_float = image_bgr.astype(np.float32) / 255.0
    corrected = image_float @ matrix.T
    corrected = np.clip(corrected, 0.0, 1.0)
    return (corrected * 255.0).astype(np.uint8)


def apply_gamma(image_bgr, gamma):
    """Gamma correction。"""
    image_float = image_bgr.astype(np.float32) / 255.0
    corrected = image_float ** gamma
    return np.clip(corrected * 255.0, 0, 255).astype(np.uint8)


def apply_reinhard_tone_mapping(image_bgr, exposure):
    """简单 Reinhard tone mapping，并尽量保持原来的颜色比例。"""
    image_float = image_bgr.astype(np.float32) / 255.0
    blue, green, red = cv2.split(image_float)

    # 先算亮度，再只压缩亮度；这样比直接压 B/G/R 三个通道更不容易偏色。
    luminance = 0.114 * blue + 0.587 * green + 0.299 * red
    x = luminance * exposure
    mapped_luminance = x / (1.0 + x)
    scale = mapped_luminance / np.maximum(luminance, 1e-6)

    mapped = image_float * scale[:, :, None]
    return np.clip(mapped * 255.0, 0, 255).astype(np.uint8)


def run_raw_to_rgb_demo(image_bgr, blue_gain, green_gain, red_gain, color_style, gamma, exposure, demosaic_method, pre_blur_size):
    """运行完整 RAW-to-RGB demo，并返回每一步结果。"""
    input_bgr = resize_for_demo(image_bgr)
    raw_source_bgr = blur_before_bayer(input_bgr, pre_blur_size)
    bayer_raw = simulate_rggb_bayer(raw_source_bgr)

    if demosaic_method == "simple":
        demosaic_bgr = demosaic_simple(bayer_raw)
    else:
        demosaic_bgr = demosaic_opencv(bayer_raw)

    white_balance = apply_white_balance(demosaic_bgr, blue_gain, green_gain, red_gain)
    color_matrix = get_color_matrix(color_style)
    color_corrected = apply_color_matrix(white_balance, color_matrix)
    gamma_image = apply_gamma(color_corrected, gamma)
    tone_mapped = apply_reinhard_tone_mapping(gamma_image, exposure)

    return {
        "input_bgr": input_bgr,
        "raw_source_bgr": raw_source_bgr,
        "bayer_raw": bayer_raw,
        "demosaic_bgr": demosaic_bgr,
        "white_balance": white_balance,
        "color_corrected": color_corrected,
        "gamma": gamma_image,
        "tone_mapped": tone_mapped,
    }


def main():
    """读取输入图，运行 RAW-to-RGB demo，并保存结果。"""
    parser = argparse.ArgumentParser(description="RAW-to-RGB demo")
    parser.add_argument("--image", type=str, default=str(default_image_path), help="输入图片路径")
    parser.add_argument("--demosaic", choices=["opencv", "simple"], default="opencv", help="demosaic 方法")
    parser.add_argument("--pre-blur-size", type=int, default=3, help="Bayer 抽样前的轻微模糊核大小")
    parser.add_argument("--blue-gain", type=float, default=1.00, help="蓝色通道增益")
    parser.add_argument("--green-gain", type=float, default=1.00, help="绿色通道增益")
    parser.add_argument("--red-gain", type=float, default=1.00, help="红色通道增益")
    parser.add_argument("--color-style", choices=["identity", "warm", "cool", "vivid"], default="identity", help="颜色校正矩阵风格")
    parser.add_argument("--gamma", type=float, default=1.0, help="gamma correction 参数")
    parser.add_argument("--exposure", type=float, default=2.0, help="tone mapping 曝光系数")
    args = parser.parse_args()

    image_path = Path(args.image)
    image_bgr = read_image_bgr(image_path)
    if image_bgr is None:
        raise FileNotFoundError(f"图片读取失败: {image_path}")

    results = run_raw_to_rgb_demo(
        image_bgr,
        blue_gain=args.blue_gain,
        green_gain=args.green_gain,
        red_gain=args.red_gain,
        color_style=args.color_style,
        gamma=args.gamma,
        exposure=args.exposure,
        demosaic_method=args.demosaic,
        pre_blur_size=args.pre_blur_size,
    )

    cv2.imwrite(str(output_dir / "01_input_bgr.png"), results["input_bgr"])
    cv2.imwrite(str(output_dir / "01_raw_source_bgr.png"), results["raw_source_bgr"])
    cv2.imwrite(str(output_dir / "02_fake_bayer_raw.png"), results["bayer_raw"])
    cv2.imwrite(str(output_dir / "03_demosaic_bgr.png"), results["demosaic_bgr"])
    cv2.imwrite(str(output_dir / "04_white_balance.png"), results["white_balance"])
    cv2.imwrite(str(output_dir / "05_color_corrected.png"), results["color_corrected"])
    cv2.imwrite(str(output_dir / "06_gamma.png"), results["gamma"])
    cv2.imwrite(str(output_dir / "07_tone_mapped.png"), results["tone_mapped"])

    bayer_preview = cv2.cvtColor(results["bayer_raw"], cv2.COLOR_GRAY2BGR)
    compare = np.hstack(
        [
            add_label(results["input_bgr"], "Input"),
            add_label(bayer_preview, "Fake Bayer"),
            add_label(results["demosaic_bgr"], "Demosaic"),
            add_label(results["white_balance"], "White Balance"),
            add_label(results["color_corrected"], "Color Matrix"),
            add_label(results["gamma"], "Gamma"),
            add_label(results["tone_mapped"], "Tone Mapping"),
        ]
    )
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输入图片:", image_path)
    print("输出目录:", output_dir)
    print("已保存: 01_input_bgr.png 到 07_tone_mapped.png，以及 compare.png")


if __name__ == "__main__":
    main()
