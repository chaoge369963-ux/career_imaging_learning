# 第 0 周：环境与第一课

## 已完成

- 创建 `career_imaging_learning` 学习目录结构。
- 创建 Conda 环境 `imaging_learning`。
- 安装 `numpy`、`matplotlib`、`opencv-python`、`torch`、`torchvision`。
- 新增 `AGENTS.md`，约束 Codex 只做小步教学，不碰 `RL_SNN3` 主线代码。
- 跑通第一课：读取图片、转灰度、画灰度直方图。

## 环境信息

环境路径：

```text
D:\study\app\anaconda3\envs\imaging_learning
```

用户平时可以这样用：

```powershell
conda activate imaging_learning
python 01_opencv_basic/01_read_gray_hist.py
```

如果 `conda run` 遇到中文输出编码问题，可以直接调用环境里的 Python：

```powershell
D:\study\app\anaconda3\envs\imaging_learning\python.exe 01_opencv_basic/01_read_gray_hist.py
```

## 第一课输出

```text
01_opencv_basic/outputs/01_read_gray_hist/
  demo_input.png
  original.png
  gray.png
  histogram.png
```

## 今天学会了

1. 图片在 Python 里是一个数组。
2. 彩色图 shape 通常是 `H x W x 3`。
3. 灰度图 shape 是 `H x W`。
4. OpenCV 读取彩色图时默认是 `BGR` 通道顺序。
5. 直方图表示像素亮度分布。
