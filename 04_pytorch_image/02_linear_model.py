# -*- coding: utf-8 -*-
"""
PyTorch 图像学习第 2 课：nn.Linear 和输出 shape。

这一课只做一件事：
    把一批小图像 N,C,H,W 展平成 N,F，再送进 nn.Linear。
"""

import torch


def make_toy_batch():
    """生成一批假图像：N=2, C=3, H=2, W=2。"""
    tensor_nchw = torch.tensor(
        [
            [
                [[1.0, 0.0], [0.0, 1.0]],
                [[0.0, 1.0], [1.0, 0.0]],
                [[0.5, 0.5], [0.5, 0.5]],
            ],
            [
                [[0.2, 0.2], [0.8, 0.8]],
                [[0.1, 0.9], [0.1, 0.9]],
                [[1.0, 0.0], [1.0, 0.0]],
            ],
        ],
        dtype=torch.float32,
    )
    return tensor_nchw


def flatten_image_batch(tensor_nchw):
    """把 N,C,H,W 展平成 N,F。"""
    # TODO: 变量名建议：batch_size, tensor_nf
    batch_size = tensor_nchw.shape[0]
    tensor_nf = tensor_nchw.view(batch_size,-1)
    return tensor_nf

    raise NotImplementedError("请你完成 flatten_image_batch()")


def build_linear_model(in_features, out_features):
    """创建一个最简单的线性层。"""
    # TODO: 变量名建议：linear
    linear = torch.nn.Linear(in_features, out_features)
    return linear
    raise NotImplementedError("请你完成 build_linear_model()")


def run_model(linear, tensor_nf):
    """把 N,F 输入 linear，得到 N,out_features。"""
    # TODO: 变量名建议：output
    out_features = linear(tensor_nf)
    return out_features
    raise NotImplementedError("请你完成 run_model()")


def print_tensor_info(name, tensor):
    """打印 tensor 的基本信息。"""
    print(name)
    print("  shape:", tensor.shape)
    print("  dtype:", tensor.dtype)
    print("  device:", tensor.device)


def main():
    """运行第 2 课。"""
    torch.manual_seed(0)

    tensor_nchw = make_toy_batch()
    print_tensor_info("1. 原始图像 batch: N,C,H,W", tensor_nchw)

    tensor_nf = flatten_image_batch(tensor_nchw)
    print_tensor_info("2. 展平后: N,F", tensor_nf)

    in_features = tensor_nf.shape[1]
    out_features = 4
    linear = build_linear_model(in_features, out_features)
    print("3. Linear 层:", linear)

    output = run_model(linear, tensor_nf)
    print_tensor_info("4. Linear 输出: N,out_features", output)
    print("输出数值：")
    print(output)


if __name__ == "__main__":
    main()
