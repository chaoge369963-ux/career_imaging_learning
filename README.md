# career_imaging_learning

这是成像算法 / AI for Imaging 的就业副线学习仓库。

主线目标很朴素：先把 Python、NumPy、OpenCV、PyTorch 练到能做小实验，再把这些小实验整理成可以展示的项目。

## 当前学习边界

- 不修改 `RL_SNN3` 主线代码。
- 所有脚本尽量兼容 Python 3.8 语法。
- 每个脚本都写中文注释，优先让初学者看懂。
- 每次只做一个小任务：能运行、能保存结果、能解释清楚。
- 输出图片统一放在对应章节的 `outputs/` 目录。

## 环境

环境名：

```powershell
conda activate imaging_learning
```

已安装的核心包：

```text
numpy
matplotlib
opencv-python
torch
torchvision
```

## 目录

```text
00_python_basic/      Python 和 NumPy 基础
01_opencv_basic/      OpenCV 读图、灰度、直方图、滤波、锐化
02_mini_isp/          最小 ISP：Bayer、demosaic、白平衡、gamma
03_raw_to_rgb/        RAW 到 RGB 的流程演示
04_pytorch_image/     PyTorch 图像增强小模型
05_notes/             每周复盘和概念笔记
06_image_restoration_basic/ 传统图像复原：卷积、滤波、锐化、去模糊
```

## 第一课

先运行：

```powershell
python 01_opencv_basic/01_read_gray_hist.py
```

如果在 Codex 或终端里 `conda run` 遇到中文编码问题，可以直接运行：

```powershell
D:\study\app\anaconda3\envs\imaging_learning\python.exe 01_opencv_basic/01_read_gray_hist.py
```

这节课只学 5 件事：

1. 图片在 Python 里是一个数组。
2. 彩色图 shape 通常是 `H x W x 3`。
3. 灰度图 shape 是 `H x W`。
4. 直方图表示像素亮度分布。
5. 图像处理本质是对数组做变换。
