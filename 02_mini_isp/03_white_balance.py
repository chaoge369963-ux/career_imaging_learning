# -*- coding: utf-8 -*-
"""
mini ISP 第三课：白平衡。

运行方式：
    python 02_mini_isp/03_white_balance.py

本课核心函数：
    apply_white_balance(image_bgr, blue_gain, green_gain, red_gain)
"""

from pathlib import Path

import cv2
import numpy as np


script_dir = Path(__file__).resolve().parent
input_dir = script_dir / "outputs" / "02_demosaic_simple"
output_dir = script_dir / "outputs" / "03_white_balance"
output_dir.mkdir(parents=True, exist_ok=True)

input_path = input_dir / "demosaic_bgr.png"


def add_label(image_bgr, label):
    """在图片左上角写标签，方便看对比图。"""
    labeled = image_bgr.copy()
    cv2.rectangle(labeled, (0, 0), (260, 42), (255, 255, 255), thickness=-1)
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


def create_color_cast(image_bgr):
    """人为制造一张偏红偏暖的图，方便观察白平衡效果。"""
    image_float = image_bgr.astype(np.float32)
    blue, green, red = cv2.split(image_float)

    blue = blue * 0.70
    green = green * 0.95
    red = red * 1.25

    cast_bgr = cv2.merge([blue, green, red])
    cast_bgr = np.clip(cast_bgr, 0, 255).astype(np.uint8)
    return cast_bgr


def apply_white_balance(image_bgr, blue_gain, green_gain, red_gain):
    image_float = image_bgr.astype(np.float32)
    blue,green,red = cv2.split(image_float)

    blue *= blue_gain
    green *= green_gain
    red *= red_gain
    cast_bgr = cv2.merge([blue,green,red])
    cast_bgr = np.clip(cast_bgr,0,255).astype(np.uint8)
    return cast_bgr


def main():
    """读取 demosaic 图，制造偏色图，再做白平衡。"""
    demosaic_bgr = cv2.imread(str(input_path), cv2.IMREAD_COLOR)

    if demosaic_bgr is None:
        raise FileNotFoundError("找不到 demosaic_bgr.png，请先运行 02_mini_isp/02_demosaic_simple.py")

    print("输入图 shape:", demosaic_bgr.shape)
    print("输入图 dtype:", demosaic_bgr.dtype)

    cast_bgr = create_color_cast(demosaic_bgr)

    # 这里的增益是为了大致抵消 create_color_cast 里人为制造的偏色。
    corrected_bgr = apply_white_balance(
        cast_bgr,
        blue_gain=1.35,
        green_gain=1.05,
        red_gain=0.80,
    )

    print("偏色图 shape:", cast_bgr.shape)
    print("白平衡图 shape:", corrected_bgr.shape)

    compare = np.hstack(
        [
            add_label(demosaic_bgr, "Demosaic"),
            add_label(cast_bgr, "Color Cast"),
            add_label(corrected_bgr, "White Balance"),
        ]
    )

    cv2.imwrite(str(output_dir / "demosaic_bgr.png"), demosaic_bgr)
    cv2.imwrite(str(output_dir / "color_cast.png"), cast_bgr)
    cv2.imwrite(str(output_dir / "white_balance.png"), corrected_bgr)
    cv2.imwrite(str(output_dir / "compare.png"), compare)

    print("输出目录:", output_dir)
    print("已保存: demosaic_bgr.png, color_cast.png, white_balance.png, compare.png")


if __name__ == "__main__":
    main()
