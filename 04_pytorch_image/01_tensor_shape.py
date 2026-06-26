# -*- coding: utf-8 -*-
"""
PyTorch 图像学习第 1 课：Tensor shape。

这一课只做一件事：
    NumPy 图像 H,W,C -> PyTorch 图像 C,H,W -> 模型输入 N,C,H,W
"""

import numpy as np
import torch


def make_toy_image():
    """生成一张很小的假彩色图，方便看 shape。"""
    image_hwc = np.array(
        [
            [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
            [[255, 255, 0], [0, 255, 255], [255, 0, 255]],
        ],
        dtype=np.uint8,
    )
    return image_hwc


def to_float01(image_uint8):
    """把 0-255 的 uint8 图像转成 0-1 的 float32 图像。"""
    image_float = image_uint8.astype(np.float32) / 255
    return image_float


def hwc_to_chw_tensor(image_float):
    """把 NumPy 的 H,W,C 图像转成 PyTorch 的 C,H,W tensor。"""
    tensor_hwc = torch.as_tensor(image_float)
    tensor_chw = tensor_hwc.permute(2, 0, 1)
    return tensor_chw


def add_batch_dim(tensor_chw):
    """把 C,H,W 变成 N,C,H,W，其中 N 表示 batch 数量。"""
    tensor_nchw = tensor_chw.unsqueeze(0)
    return tensor_nchw


def print_info(name, data):
    """打印 shape、dtype 和数值范围。"""
    print(name)
    print("  type:", type(data))
    print("  shape:", data.shape)
    print("  dtype:", data.dtype)

    if isinstance(data, torch.Tensor):
        print("  device:", data.device)
        print("  min:", float(data.min()))
        print("  max:", float(data.max()))
    else:
        print("  min:", float(data.min()))
        print("  max:", float(data.max()))


def main():
    """运行第一课。"""
    image_hwc = make_toy_image()
    print_info("1. NumPy 原图 H,W,C", image_hwc)

    image_float = to_float01(image_hwc)
    print_info("2. NumPy 归一化后 H,W,C", image_float)

    tensor_chw = hwc_to_chw_tensor(image_float)
    print_info("3. PyTorch 图像 C,H,W", tensor_chw)

    tensor_nchw = add_batch_dim(tensor_chw)
    print_info("4. PyTorch 模型输入 N,C,H,W", tensor_nchw)


if __name__ == "__main__":
    main()
