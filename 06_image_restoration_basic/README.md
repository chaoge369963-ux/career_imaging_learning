# 06_image_restoration_basic

这一阶段学习传统图像复原基础：卷积、滤波、锐化、模糊和简单去模糊。

## 阶段目标

你要先理解一个核心事实：

```text
很多图像增强和复原操作，本质上都是用 kernel 对图像做卷积。
```

## 第 1 课：卷积核

脚本：

```text
01_convolution_kernel_practice.py
```

运行命令：

```powershell
python 06_image_restoration_basic/01_convolution_kernel_practice.py
```

调整均值滤波核大小：

```powershell
python 06_image_restoration_basic/01_convolution_kernel_practice.py --kernel-size 3
python 06_image_restoration_basic/01_convolution_kernel_practice.py --kernel-size 9
```

输出目录：

```text
06_image_restoration_basic/outputs/01_convolution_kernel_practice/
  01_input.png
  02_box_blur.png
  03_sharpen.png
  compare.png
```

## 这一课要理解

```text
box kernel：邻域平均，会让图像变模糊
sharpen kernel：增强中心像素和周围差异，会让边缘更明显
kernel sum：均值滤波核的和应该是 1
filter2D：OpenCV 里执行卷积/滤波的 API
```

## 下一步

完成 `make_box_kernel()`，运行脚本，观察 `kernel-size` 从 3 到 9 时图像模糊程度怎么变化。

## 第 2 课：亮度锐化

脚本：

```text
02_luminance_sharpen_practice.py
```

运行命令：

```powershell
python 06_image_restoration_basic/02_luminance_sharpen_practice.py
```

切换到 8 邻域锐化核：

```powershell
python 06_image_restoration_basic/02_luminance_sharpen_practice.py --kernel-type 8
```

输出目录：

```text
06_image_restoration_basic/outputs/02_luminance_sharpen_practice/
  01_input.png
  02_bgr_direct_sharpen.png
  03_luminance_only_sharpen.png
  compare.png
```

这一课要理解：

```text
BGR Sharpen：分别锐化 B/G/R 三个通道，可能改变颜色比例
Y-only Sharpen：只锐化亮度通道，更不容易产生色偏
4 邻域锐化：温和一点
8 邻域锐化：更强，但更容易放大噪声和边缘伪影
```

## 第 3 课：Unsharp Mask 反差保留锐化

脚本：

```text
03_unsharp_mask_practice.py
```

运行命令：

```powershell
python 06_image_restoration_basic/03_unsharp_mask_practice.py
```

调整锐化强度：

```powershell
python 06_image_restoration_basic/03_unsharp_mask_practice.py --amount 0.8
python 06_image_restoration_basic/03_unsharp_mask_practice.py --amount 2.0
```

调整细节尺度：

```powershell
python 06_image_restoration_basic/03_unsharp_mask_practice.py --blur-size 5
python 06_image_restoration_basic/03_unsharp_mask_practice.py --blur-size 15
```

输出目录：

```text
06_image_restoration_basic/outputs/03_unsharp_mask_practice/
  01_input.png
  02_detail_layer.png
  03_unsharp_mask.png
  compare.png
```

这一课要理解：

```text
blurred：低频图，保留大轮廓
detail = original - blurred：高频细节
sharpen = original + amount * detail：把细节加回去
amount 越大，锐化越强，也越容易出现噪声和边缘光晕
```

## 第 4 课：运动模糊与简单恢复

脚本：

```text
04_motion_blur_restore_practice.py
```

运行命令：

```powershell
python 06_image_restoration_basic/04_motion_blur_restore_practice.py
```

调整运动模糊长度：

```powershell
python 06_image_restoration_basic/04_motion_blur_restore_practice.py --motion-size 9
python 06_image_restoration_basic/04_motion_blur_restore_practice.py --motion-size 21
```

调整恢复锐化强度：

```powershell
python 06_image_restoration_basic/04_motion_blur_restore_practice.py --amount 2.2
```

输出目录：

```text
06_image_restoration_basic/outputs/04_motion_blur_restore_practice/
  01_input.png
  02_motion_blur.png
  03_unsharp_restore.png
  compare.png
```

这一课要理解：

```text
motion blur kernel：模拟相机或物体运动造成的方向性模糊
PSNR：用数值比较结果和原图的差异
Unsharp Mask 可以让模糊图看起来更清楚
但看起来更清楚，不一定代表真实细节被恢复
```

## 第 5 课：噪声与去噪

脚本：

```text
05_noise_denoise_practice.py
```

运行命令：

```powershell
python 06_image_restoration_basic/05_noise_denoise_practice.py
```

调噪声强度：

```powershell
python 06_image_restoration_basic/05_noise_denoise_practice.py --noise-sigma 35
```

调滤波核大小：

```powershell
python 06_image_restoration_basic/05_noise_denoise_practice.py --kernel-size 3
python 06_image_restoration_basic/05_noise_denoise_practice.py --kernel-size 7
```

输出目录：

```text
06_image_restoration_basic/outputs/05_noise_denoise_practice/
  01_input.png
  02_noisy.png
  03_mean_denoised.png
  04_gaussian_denoised.png
  compare.png
```

这一课要理解：

```text
噪声：随机扰动
去噪：平滑随机扰动
代价：细节也可能被抹掉
PSNR：数值上比较谁更接近原图
```

## 第 6 课：去噪后再轻微锐化

脚本：

```text
06_denoise_then_sharpen_practice.py
```

运行命令：

```powershell
python 06_image_restoration_basic/06_denoise_then_sharpen_practice.py
```

调锐化强度：

```powershell
python 06_image_restoration_basic/06_denoise_then_sharpen_practice.py --amount 1.2
```

输出目录：

```text
06_image_restoration_basic/outputs/06_denoise_then_sharpen_practice/
  01_input.png
  02_noisy.png
  03_denoised.png
  04_denoise_then_sharpen.png
  compare.png
```

这一课要理解：

```text
先去噪：压随机噪声
再轻微锐化：补一点边缘清晰感
锐化太强：噪声和伪影会回来
```

## 阶段 TODO：请你自己回答

这一部分不用写得很学术，先用自己的话回答。

### 1. 卷积核是什么？

我的回答：实际上就是一个n乘n的矩阵


### 2. 模糊为什么会损失细节？

我的回答：会把原本的高频信息降低从而损失信息


### 3. 锐化为什么会让边缘更明显？

我的回答：边缘高频信息多，锐化会加强高频信息

### 4. 为什么锐化也会放大噪声？

我的回答：噪声也是信息的一种，高频噪声会因为锐化变得更加明显


### 5. 去噪为什么会让图像变糊？

我的回答：去噪本质是使噪声减低，用模糊的办法去噪会导致图像变糊


### 6. PSNR 越大说明什么？

我的回答：越大说明和原图的色彩颜色差别越小


### 7. 这一阶段你最有感觉的是哪个实验？

我的回答：最图像锐化吧，尤其是先模糊提取高频信息在叠加回去


### 8. 用一句话总结传统图像复原

我的回答：用blur锐化的方法消除噪声，增强细节


## 阶段过关标准

你写完上面的回答后，至少要能讲清楚：

```text
图像增强不等于真实恢复。
去噪会压掉随机噪声，但也可能损失细节。
锐化能增强边缘清晰感，但也可能放大噪声和伪影。
PSNR 是一个参考指标，不能完全代替人眼观察。
```
