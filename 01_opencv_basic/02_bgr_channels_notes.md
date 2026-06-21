# 第二课：BGR 三通道

## 目标

理解彩色图 `shape = H x W x 3` 里面最后的 `3` 是什么。

## 运行命令

```powershell
python 01_opencv_basic/02_bgr_channels.py
```

如果中文输出或 `conda run` 有问题，可以直接用环境里的 Python：

```powershell
D:\study\app\anaconda3\envs\imaging_learning\python.exe 01_opencv_basic/02_bgr_channels.py
```

## 输出位置

```text
01_opencv_basic/outputs/02_bgr_channels/
  original.png
  blue_channel_gray.png
  green_channel_gray.png
  red_channel_gray.png
  blue_only.png
  green_only.png
  red_only.png
```

## 今天要理解

彩色图不是一个数字，而是每个像素有 3 个数字。

在 OpenCV 里，这 3 个数字的顺序是：

```text
B 蓝色
G 绿色
R 红色
```

所以彩色图的 shape 通常是：

```text
H x W x 3
```

灰度图的 shape 通常是：

```text
H x W
```

因为灰度图每个像素只有一个亮度数字。
