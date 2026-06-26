# 03_raw_to_rgb 阶段复盘

这一页是给你自己填写的，不要求写得高级，先用自己的话讲清楚。

## 1. 这个阶段做了什么

请用 3 到 5 句话说明：

```text
我这一阶段完成了：
1.raw图变成彩色图
2.色调调整
3.黑电平衡
4、曝光区域裁剪
5、算裁剪范围
6、算合理裁剪和平均裁剪


```

## 2. RAW-to-RGB 流程

请按顺序解释每一步在干什么：

```text
Fake Bayer:把原始图片变成一个相机最开始接收的拜尔原始图像

Demosaic:把拜尔原始图像变成彩色图

White Balance:调整三个颜色强度到眼睛适合的强度

Color Correction Matrix:调整颜色风格

Gamma:幂函数调整颜色强度曲线

Tone Mapping:是图片整体光强在显示范围

Black/White Level Normalize:去掉在显示范围外的参数

Exposure Gain:增加图像亮度


Auto Exposure:调节合适的曝光防止过曝

Highlight Protection:防止图像因为过量大部分像素点都变成白色不显示颜色了
```

## 3. 我现在能讲清楚的概念

把你觉得已经理解的打勾：

```text
[√ ] Bayer RAW 为什么是单通道
[ ] Demosaic 为什么会产生彩边
[ √] White Balance 是调 B/G/R 三个通道增益
[ √] Color Matrix 是重新混合 B/G/R
[ √] Gamma 会改变显示亮度
[ √] Tone Mapping 会压缩高亮
[ √] RAW 黑电平不是 0
[ √] RAW 白电平可能是 4095 或 16383
[ √] 归一化公式是 (raw - black) / (white - black)
[ √] exposure gain 会让图变亮
[ √] clipped ratio 表示过曝比例
[√ ] auto exposure 可以根据平均亮度算 gain
[√ ] highlight protection 会限制过曝比例
```

## 4. 我还没完全懂的地方

请直接写，不用怕低级：

```text
我还不太懂：
1.我知道去马赛克会产生彩色条纹，因为颜色恢复的不是完全准确，但是我不太会描述为什么
2.过曝比例就是超过归一化1的吧，为什么不记录低于0的
3.感觉整个项目还没结束吧，怎么就收尾了
```

## 5. 一个面试版项目描述草稿

先自己写一版，后面我帮你润色：

```text
我实现了图片的bayer_raw变成彩图的过程，同时对彩图调整色调，整体亮度，设计了自动设置曝光系数还有防爆光
```

## 6. 下一步想做什么

选一个：

```text
[ ] 把 03_raw_to_rgb README 改成作品集版本
[ √] 进入传统图像复原：卷积、滤波、锐化、去模糊
[ ] 进入 PyTorch 图像去噪
[ ] 回头整理 GitHub 提交
```
