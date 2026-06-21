# 01_opencv_basic

这是 OpenCV 基础图像处理阶段的小项目。

本阶段目标不是背函数，而是理解：

- 图片在 Python 里是数组。
- 彩色图通常是 `H x W x 3`。
- 灰度图通常是 `H x W`。
- 图像处理就是对像素数组做变换。
- 评价图像结果时，既要看图，也要看指标。

## 运行环境

```powershell
conda activate imaging_learning
```

如果终端中文输出有问题，可以直接使用环境里的 Python：

```powershell
D:\study\app\anaconda3\envs\imaging_learning\python.exe 01_opencv_basic/08_before_after_grid.py
```

## 脚本清单

```text
01_read_gray_hist.py       读图、转灰度、画直方图
02_bgr_channels.py        拆分 B/G/R 三个颜色通道
03_gray_hist_by_hand.py   手写版读图、转灰度、画直方图
04_blur_compare.py        比较均值模糊和高斯模糊
05_sharpen_kernel.py      用卷积核做锐化
06_noise_and_psnr.py      添加高斯噪声并计算 PSNR
07_denoise_compare.py     均值/高斯滤波去噪，并扫描不同 kernel_size
08_before_after_grid.py   汇总前面结果，生成总览图
```

## 主要输出

总览图：

```text
outputs/08_before_after_grid/opencv_basic_summary.png
```

PSNR 曲线：

```text
outputs/07_denoise_compare/psnr_curve.png
```

去噪对比图：

```text
outputs/07_denoise_compare/compare_3.png
outputs/07_denoise_compare/compare_5.png
outputs/07_denoise_compare/compare_7.png
outputs/07_denoise_compare/compare_9.png
```

## 我的阶段总结

### 1. 我做了什么

回答：

```text
这一阶段我用 OpenCV 做了一组基础图像处理实验：读取彩色图、转换灰度图、拆分 B/G/R 通道、画灰度直方图、做模糊和锐化处理。
之后我给图像添加高斯噪声，用 PSNR 比较噪声图和去噪图，并尝试不同 kernel_size 对去噪效果的影响。
最后我把主要结果拼成一张总览图，用来回顾这一阶段的实验结果。
```

### 2. 图片为什么是数组

问题：

```text
为什么说图片在 Python 里是一组数字？
彩色图 shape = H x W x 3 中，最后的 3 表示什么？
灰度图为什么没有最后的 3？
```

回答：

```text
图片本质上是很多像素点组成的，每个像素可以用数字表示亮度或颜色强度。
灰度图中，每个像素通常是 0 到 255 之间的一个数字，0 接近黑色，255 接近白色。
彩色图 shape = H x W x 3，其中 H 是高度，W 是宽度，最后的 3 表示 B/G/R 三个颜色通道。
灰度图没有最后的 3，是因为它只有一个亮度通道，不再分别存储蓝、绿、红三个颜色通道。
```

### 3. BGR 和 RGB

问题：

```text
OpenCV 读入彩色图时，通道顺序是什么？
BGR 三个字母分别代表什么？
为什么 blue_channel_gray.png 是黑白图，但 blue_only.png 是蓝色图？
```

回答：

```text
OpenCV 读入彩色图时，默认通道顺序是 BGR，也就是蓝、绿、红。
blue_channel_gray.png 是黑白图，因为它只是把蓝色通道的数值当作灰度强弱显示，亮的地方表示蓝色数值大。
blue_only.png 是蓝色图，因为它保留了蓝色通道，把绿色和红色通道清零，所以显示出来就是蓝色效果。
这个实验让我理解到：通道本身是数字矩阵，显示成什么颜色取决于我们怎么展示它。
```

### 4. 直方图

问题：

```text
灰度直方图统计的是什么？
为什么画直方图前可以用 image_gray.ravel()？
如果直方图集中在左边，图像一般偏暗还是偏亮？
```

回答：

```text
灰度直方图统计的是不同亮度值的像素数量。
`image_gray.ravel()` 可以把 H x W 的二维灰度图拉平成一串像素数字，方便 `plt.hist()` 统计亮度分布。
如果直方图集中在左边，说明低亮度像素更多，图像一般偏暗；如果集中在右边，图像一般偏亮。
```

### 5. 模糊和锐化

问题：

```text
kernel_size = (5, 5) 表示什么？
均值模糊和高斯模糊有什么区别？
为什么先模糊再锐化，通常不能完全还原原图？
```

回答：

```text
`kernel_size = (5, 5)` 表示处理每个像素时，会参考它周围 5 x 5 的局部区域。
均值模糊是把局部窗口内的像素简单求平均；高斯模糊也是局部模糊，但中心附近的像素权重更大，离中心远的像素权重更小，所以通常更自然。
先模糊再锐化通常不能完全还原原图，因为模糊会损失一部分边缘和细节信息。
锐化只能增强当前图像里还存在的边缘和高频信息，不能凭空创造已经丢失的真实细节。
```

### 6. 噪声、去噪和 PSNR

问题：

```text
高斯噪声是什么？
为什么加噪声后要 clip 到 0-255？
PSNR 衡量的是什么？
PSNR 越高一定代表图像主观上越好吗？
```

回答：

```text
高斯噪声可以理解成加在像素值上的随机扰动，图像里会出现随机的亮暗变化或颜色扰动。
加噪声后要 `clip` 到 0-255，是因为 8bit 图像的像素范围只能在 0 到 255 之间，超过这个范围就不能正确表示图像亮度。
PSNR 衡量的是两张图像在像素数值上的接近程度。PSNR 越高，通常说明和参考图像越接近，噪声或失真越小。
但是 PSNR 越高不一定代表主观视觉上一定最好，因为它主要看像素差，不完全等同于人眼感受。
```

### 7. 参数实验结论

问题：

```text
在你的 07_denoise_compare.py 实验里：
均值滤波最佳 kernel_size 是多少？
高斯滤波最佳 kernel_size 是多少？
kernel 太小时会发生什么？
kernel 太大时会发生什么？
```

回答：

```text
在我的实验里，均值滤波最佳 kernel_size 是 5x5，PSNR 约为 28.56。
高斯滤波最佳 kernel_size 是 7x7，PSNR 约为 29.01。
kernel 太小时，参考的邻域太小，去噪不够明显；kernel 太大时，虽然噪声会减少，但图像细节也会被抹掉，整体变得过于模糊。
所以去噪不是 kernel 越大越好，需要在去噪强度和细节保留之间折中。
```

### 8. 我踩过的坑

问题：

```text
这阶段你遇到过哪些报错？
比如 tuple 没有 copy、GaussianBlur 少参数、PSNR 公式写错。
这些错误分别说明了什么？
```

回答：

```text
1. `GaussianBlur` 少参数：我一开始只传了图像和 kernel_size，但 OpenCV 的高斯模糊函数还需要 `sigmaX` 参数。后来补上 `0`，让 OpenCV 自动计算。
2. PSNR 公式写错：我一开始没有先正确计算 MSE，也没有注意 uint8 相减的问题。后来先把图像转成 float，再计算 MSE 和 PSNR。
3. `tuple` 没有 `copy`：在拼总览图时，我的函数返回了三个通道组成的 tuple，而后面的 `add_label()` 需要的是一张完整图像数组。这让我理解了函数返回值类型很重要。
```

### 9. 我学到了什么

回答：

```text
BGR 彩色图和灰度图的 shape 不一样。
通道本身是数字矩阵，显示方式可以不同。
模糊可以降低噪声，但也会损失细节。
锐化可以增强边缘，但不能恢复已经丢失的信息。
PSNR 可以评价图像和参考图像的像素差异，但需要结合肉眼观察。
```

## 阶段验收

完成本阶段时，应该能做到：

- 能解释 `image.shape` 的含义。
- 能用 OpenCV 读图、存图、转灰度。
- 能拆 B/G/R 通道。
- 能做模糊、锐化、加噪声、去噪。
- 能计算并解释 PSNR。公式还需要查，但已经理解它和 MSE、图像差异有关。
- 能用结果图和曲线说明实验结论。

当前感受：

```text
我大概知道这些基础处理分别是什么，但还需要进入具体项目，才能更清楚它们在真实成像任务里怎么使用。
```
