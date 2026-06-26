# -*- coding: utf-8 -*-
"""
PyTorch 图像学习第 6 课：制作 noisy-clean 图像数据对。

这一课只做一件事：
    用 Dataset 返回一对 tensor：noisy_image, clean_image。
"""

from pathlib import Path

import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset


script_dir = Path(__file__).resolve().parent
output_dir = script_dir / "outputs" / "06_make_noisy_dataset"
output_dir.mkdir(parents=True, exist_ok=True)


def make_clean_image(height=64, width=64):
    """生成一张简单的干净 RGB 图像。"""
    x = np.linspace(0, 255, width, dtype=np.float32)
    y = np.linspace(0, 255, height, dtype=np.float32)
    grid_x, grid_y = np.meshgrid(x, y)

    red = grid_x
    green = grid_y
    blue = 255 - grid_x * 0.5 - grid_y * 0.5
    image_rgb = np.stack([red, green, blue], axis=2)
    image_rgb = np.clip(image_rgb, 0, 255).astype(np.uint8)
    return image_rgb


def rgb_uint8_to_tensor_chw(image_rgb):
    """把 RGB uint8 图像转成 C,H,W 的 float32 tensor。"""
    image_float = image_rgb.astype(np.float32) / 255.0
    tensor_hwc = torch.as_tensor(image_float)
    tensor_chw = tensor_hwc.permute(2, 0, 1)
    return tensor_chw


def add_noise_to_tensor(clean_tensor, noise_sigma):
    """给 0-1 的 clean tensor 添加高斯噪声，并裁剪回 0-1。"""
    noise = torch.randn_like(clean_tensor) * noise_sigma
    noisy_tensor = noise + clean_tensor
    noisy_tensor = torch.clamp(noisy_tensor, 0.0, 1.0)
    return noisy_tensor


class NoisyCleanDataset(Dataset):
    """每次返回一对 noisy-clean 图像 tensor。"""

    def __init__(self, clean_tensor, num_samples, noise_sigma):
        self.clean_tensor = clean_tensor
        self.num_samples = num_samples
        self.noise_sigma = noise_sigma

    def __len__(self):
        """返回数据集里有多少个样本。"""
        return self.num_samples
        

    def __getitem__(self, index):
        """返回第 index 个样本：noisy_tensor, clean_tensor。"""
        clean_tensor = self.clean_tensor
        noisy_tensor = add_noise_to_tensor(clean_tensor, self.noise_sigma)
        return noisy_tensor, clean_tensor


def tensor_chw_to_rgb_uint8(tensor_chw):
    """把 C,H,W tensor 转回 RGB uint8 图像，方便保存查看。"""
    tensor_chw = tensor_chw.detach().cpu().clamp(0, 1)
    image_hwc = tensor_chw.permute(1, 2, 0).numpy()
    image_rgb = (image_hwc * 255).astype(np.uint8)
    return image_rgb


def save_preview(noisy_tensor, clean_tensor):
    """保存 noisy 和 clean 的对比图。"""
    noisy_rgb = tensor_chw_to_rgb_uint8(noisy_tensor)
    clean_rgb = tensor_chw_to_rgb_uint8(clean_tensor)

    compare_rgb = np.hstack([clean_rgb, noisy_rgb])
    compare_bgr = cv2.cvtColor(compare_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(output_dir / "clean_noisy_compare.png"), compare_bgr)


def main():
    """运行第 6 课。"""
    torch.manual_seed(0)

    clean_rgb = make_clean_image()
    clean_tensor = rgb_uint8_to_tensor_chw(clean_rgb)

    dataset = NoisyCleanDataset(clean_tensor, num_samples=8, noise_sigma=0.12)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=False)

    noisy_batch, clean_batch = next(iter(dataloader))

    print("clean_tensor shape:", clean_tensor.shape)
    print("noisy_batch shape:", noisy_batch.shape)
    print("clean_batch shape:", clean_batch.shape)
    print("noisy min/max:", float(noisy_batch.min()), float(noisy_batch.max()))
    print("clean min/max:", float(clean_batch.min()), float(clean_batch.max()))

    save_preview(noisy_batch[0], clean_batch[0])
    print("已保存:", output_dir / "clean_noisy_compare.png")


if __name__ == "__main__":
    main()
