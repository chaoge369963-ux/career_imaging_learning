# 02_mini_isp

这一章学习最小 ISP 流程：从 Bayer RAW 到可显示 RGB 图像。

## 阶段计划表

```text
[x] 01_fake_bayer.py          BGR 彩色图 -> 单通道 RGGB Bayer RAW
[x] 02_demosaic_simple.py     Bayer RAW -> 简单恢复 BGR 彩色图
[x] 03_white_balance.py       调整 B/G/R 通道比例，修正偏色
[x] 04_gamma_correction.py    用 gamma 曲线调整显示亮度
[x] 05_tone_mapping.py        压缩过亮图像，让亮度更适合显示
[x] 06_mini_isp_pipeline.py   串起 fake Bayer -> demosaic -> WB -> gamma -> tone mapping
[x] README 阶段总结           写清楚最小 ISP 流程和每一步作用
```

## 第一课：模拟 RGGB Bayer

运行：

```powershell
python 02_mini_isp/01_fake_bayer.py
```

输出位置：

```text
02_mini_isp/outputs/01_fake_bayer/
  input_bgr.png
  fake_bayer_raw.png
  fake_bayer_preview.png
```

## 今天要理解

普通彩色图中，每个像素都有 3 个颜色值：

```text
B, G, R
```

Bayer RAW 中，每个像素通常只记录 1 个颜色值。

RGGB pattern 可以理解成一个 2 x 2 的重复小格子：

```text
R G
G B
```

所以这一步做的是：

```text
BGR 彩色图 -> 单通道 Bayer RAW
```

这不是真实相机 RAW，只是学习用的模拟 RAW。

## 第二课：简单 Demosaic

运行：

```powershell
python 02_mini_isp/02_demosaic_simple.py
```

输出位置：

```text
02_mini_isp/outputs/02_demosaic_simple/
  bayer_raw.png
  demosaic_bgr.png
  compare.png
```

## 第二课要理解

Bayer RAW 每个像素只有一个颜色值，所以它不是完整彩色图。

Demosaic 要做的是：

```text
单通道 Bayer RAW -> 三通道 BGR 彩色图
```

也就是把缺失的颜色估计出来。

例如：

```text
R 位置：已有 R，缺 G 和 B
G 位置：已有 G，缺 R 和 B
B 位置：已有 B，缺 R 和 G
```

这一步不追求工业级效果，只要求看懂“缺什么、补什么”。

## 第三课：白平衡

运行：

```powershell
python 02_mini_isp/03_white_balance.py
```

输出位置：

```text
02_mini_isp/outputs/03_white_balance/
  demosaic_bgr.png
  color_cast.png
  white_balance.png
  compare.png
```

## 第三课要理解

白平衡是在调不同颜色通道的比例。

如果图像偏红，可以降低红色通道，或者相对提高蓝色/绿色通道。

在 OpenCV 的 BGR 顺序里：

```text
B 通道 -> blue_gain
G 通道 -> green_gain
R 通道 -> red_gain
```

最简单的白平衡形式就是：

```text
B_new = B * blue_gain
G_new = G * green_gain
R_new = R * red_gain
```

最后要把结果限制在 0 到 255 之间，再转回 `uint8`。

## 第四课：Gamma Correction

运行：

```powershell
python 02_mini_isp/04_gamma_correction.py
```

输出位置：

```text
02_mini_isp/outputs/04_gamma_correction/
  input.png
  gamma_0.5.png
  gamma_1.0.png
  gamma_2.2.png
  compare.png
```

## 第四课要理解

Gamma correction 是一种亮度曲线变换。

它不是简单地给所有像素加同一个数，而是对归一化后的像素做幂运算：

```text
output = input ** gamma
```

其中 `input` 需要先从 0-255 转成 0-1。

直观理解：

```text
gamma < 1  通常会让暗部变亮
gamma = 1  图像基本不变
gamma > 1  通常会让图像变暗
```

最后再把 0-1 的结果乘回 255，并转成 `uint8`。

## 第五课：Tone Mapping

运行：

```powershell
python 02_mini_isp/05_tone_mapping.py
```

输出位置：

```text
02_mini_isp/outputs/05_tone_mapping/
  input.png
  over_bright_preview.png
  tone_mapped.png
  compare.png
```

## 第五课要理解

Tone mapping 可以理解成：

```text
把过亮或动态范围太大的图像，压缩到显示器能显示、肉眼更好看的范围。
```

这节课先用简单 Reinhard 形式：

```text
mapped = x / (1 + x)
```

其中 `x` 是归一化后的浮点图像，可以大于 1。

直观理解：

```text
x 很小时，mapped 接近 x，暗部变化不大
x 很大时，mapped 会逐渐接近 1，亮部被压住
```

所以 tone mapping 和 gamma 不完全一样：

```text
gamma correction 主要调整亮度曲线
tone mapping 更强调把过大的亮度范围压回可显示范围
```

## 第六课：完整 mini ISP Pipeline

运行：

```powershell
python 02_mini_isp/06_mini_isp_pipeline.py
```

输出位置：

```text
02_mini_isp/outputs/06_mini_isp_pipeline/
  01_input_bgr.png
  02_bayer_raw.png
  03_demosaic_bgr.png
  04_white_balance.png
  05_gamma.png
  06_tone_mapped.png
  compare.png
```

## 第六课要理解

Pipeline 的意思是“流水线”。

这节课不学新公式，而是把前面几步按顺序串起来：

```text
Input BGR
-> Fake Bayer RAW
-> Demosaic
-> White Balance
-> Gamma Correction
-> Tone Mapping
-> Display Image
```

你要补的函数是：

```python
run_mini_isp_pipeline(image_bgr)
```

它应该返回一个字典：

```python
{
    "input_bgr": ...,
    "bayer_raw": ...,
    "demosaic_bgr": ...,
    "white_balance": ...,
    "gamma": ...,
    "tone_mapped": ...,
}
```

这样主程序就能把每一步结果统一保存下来。

## 我的阶段总结

这一部分用于复盘 mini ISP 阶段的核心理解。

### 1. 我做了什么

回答：

```text
我完成了一个学习用的 mini ISP 流程：先把普通 BGR 彩色图模拟成单通道 RGGB Bayer RAW，再通过简单 demosaic 恢复成三通道彩色图。
之后我对图像做了白平衡、gamma correction 和 tone mapping，分别观察颜色比例、亮度曲线和过亮区域压缩的效果。
最后我把这些步骤串成一个 mini ISP pipeline，并保存每一步的中间结果和总览对比图。
```

### 2. Bayer RAW 是什么

问题：

```text
普通 BGR/RGB 彩色图和 Bayer RAW 最大区别是什么？
为什么 Bayer RAW 是单通道，而普通彩色图是三通道？
RGGB pattern 中，R/G/G/B 分别放在什么位置？
```

回答：

```text
普通 BGR/RGB 彩色图中，每个像素都有 3 个颜色值；Bayer RAW 中，每个像素通常只记录一个颜色值。
所以普通彩色图是三通道，而 Bayer RAW 是单通道。
RGGB pattern 是一个 2 x 2 重复排列：
[[R,G],
 [G,B]]。
```

### 3. Demosaic 是什么

问题：

```text
Demosaic 中文可以怎么理解？
为什么 Bayer RAW 需要 demosaic 才能变成彩色图？
在你的简单 demosaic 里，空位置是怎么补出来的？
mask 在补色时有什么作用？
```

回答：

```text
Demosaic 可以理解成“去马赛克”或“补色”。Bayer RAW 每个像素只有一个颜色值，要恢复成彩色图，就需要估计每个像素缺失的另外两个颜色。
我的简单 demosaic 方法是：先把已知的 R/G/B 采样值放回对应通道，再用周围 3 x 3 区域内已有的同色像素做平均，补空的位置。
mask 的作用是标记哪些位置原本有真实采样值，同时统计 3 x 3 范围内有多少个有效同色像素，避免把空位置也算进平均值。
```

### 4. 白平衡

问题：

```text
白平衡主要是在调整什么？
如果图像偏红，应该怎么调整 R/B/G 通道？
为什么白平衡后还要 clip 到 0-255，并转回 uint8？
```

回答：

```text
白平衡主要是在调整 B/G/R 三个颜色通道的相对比例，用来修正偏色。
如果图像偏红，说明红色通道相对太强，通常应该降低 R 通道，或者相对提高 B/G 通道。
白平衡后要 clip 到 0-255，是因为普通 8bit 图像的像素范围只能在 0 到 255 之间。
最后转回 uint8，是为了让 OpenCV 正常保存和显示普通 8bit 图片。
```

### 5. Gamma Correction

问题：

```text
Gamma correction 是调什么的？
为什么要先把图像从 0-255 转到 0-1？
gamma < 1、gamma = 1、gamma > 1 大概分别会产生什么效果？
```

回答：

```text
Gamma correction 调整的是亮度曲线，不是简单地把所有像素整体乘一个系数。
做 gamma 运算前要先把图像从 0-255 归一化到 0-1，这样 `input ** gamma` 的含义更稳定。
一般来说，gamma < 1 会让暗部变亮，gamma = 1 基本不变，gamma > 1 会让图像变暗。
```

### 6. Tone Mapping

问题：

```text
Tone mapping 中文可以怎么理解？
它和简单 clip 有什么区别？
Reinhard 公式 mapped = x / (1 + x) 为什么能压住过亮区域？
Tone mapping 和 gamma correction 有什么不同？
```

回答：

```text
Tone mapping 可以理解成色调映射或亮度范围压缩。
它和简单 clip 不一样：clip 会把超过范围的亮度直接砍掉，而 tone mapping 会用曲线把过大的亮度压回可显示范围，尽量保留亮部层次。
Reinhard 公式 `mapped = x / (1 + x)` 中，x 越大，mapped 越接近 1，但不会无限增大，所以它能压住过亮区域。
Gamma correction 主要调整亮度曲线；tone mapping 更强调把过大的动态范围压缩到屏幕可显示的范围。
```

### 7. Pipeline 流水线

问题：

```text
pipeline 在这里是什么意思？
你的 mini ISP pipeline 包含哪几步？
为什么 run_mini_isp_pipeline() 最后返回 dict 比返回 list 更清楚？
```

回答：

```text
Pipeline 在这里就是“处理流水线”，也就是把多个图像处理步骤按固定顺序串起来。
这个项目里的 mini ISP pipeline 是学习用的简化流程：Input BGR -> Fake Bayer RAW -> Demosaic -> White Balance -> Gamma Correction -> Tone Mapping。
`run_mini_isp_pipeline()` 返回 dict 比返回 list 更清楚，因为每一步结果都有名字，例如 `results["bayer_raw"]`，不用记住第几个位置对应哪一步。
```

### 8. 我踩过的坑

问题：

```text
这一阶段你遇到过哪些错误或容易混的点？
比如 0-based 索引、H x W 和 H x W x 3、list/dict、shape 和数组内容、clip 和 tone mapping。
这些错误分别说明了什么？
```

回答：

```text
1. 路径定位容易忘：`Path(__file__).resolve().parent` 的作用是找到当前脚本所在文件夹，再从这里拼输入和输出路径。
2. shape 和数组内容容易混：`image.shape = H x W x 3` 只是说明数组形状，不是图像里的像素值；真正参与计算的是数组里的每个像素数字。
3. list 和 dict 容易混：list 要用数字索引，dict 可以用名字索引。pipeline 里返回 dict 更适合保存每一步结果。
这些问题说明我还需要继续熟悉 NumPy 数组、路径管理和 Python 数据结构。
```

### 9. 我学到了什么

回答：

```text
Bayer RAW 是单通道传感器采样图。
RGGB pattern 决定不同像素位置采样哪个颜色。
Demosaic 是补全缺失颜色。
白平衡是调整 B/G/R 通道比例。
Gamma correction 是亮度曲线变换。
Tone mapping 是动态范围压缩。
Pipeline 是把多个处理步骤串成完整流程。
```

### 10. 这个小项目能怎么讲

问题：

```text
如果给别人介绍这个 mini ISP 小项目，你会怎么用 3 句话讲清楚？
输入是什么？
中间做了哪些处理？
输出结果说明了什么？
```

回答：

```text
本项目实现了一个学习用 mini ISP pipeline，输入是一张普通 BGR 彩色图，并模拟生成 RGGB Bayer RAW。
随后依次完成简单 demosaic、白平衡、gamma correction 和 tone mapping，并保存每一步中间结果。
最终输出 `compare.png`，用于观察从 Bayer RAW 到可显示图像的完整处理流程。
```

## 阶段验收

完成本阶段时，应该能做到：

- 能解释 Bayer RAW 为什么是单通道。
- 能说明 RGGB pattern 的位置规则。
- 能解释 demosaic 是在补缺失颜色。
- 能说明白平衡、gamma、tone mapping 分别在调什么。
- 能运行完整 mini ISP pipeline，并找到每一步输出图。
- 能用 `compare.png` 说明最小 ISP 流程。
