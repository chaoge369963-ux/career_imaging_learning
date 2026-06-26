# 03_raw_to_rgb

这一章把前面学过的 mini ISP 步骤整理成一个 `raw_to_rgb_demo` 小项目。

## 项目目标

输入一张普通 BGR 图片，先模拟成单通道 RGGB Bayer RAW，再依次完成：

```text
Fake Bayer RAW
-> Demosaic
-> White Balance
-> Color Correction Matrix
-> Gamma Correction
-> Tone Mapping
-> Display Image
```

这仍然是学习用模拟流程，不是真实相机 RAW 解码。

## 运行命令

使用默认练习图：

```powershell
python 03_raw_to_rgb/01_raw_to_rgb_demo.py
```

使用自己的图片：

```powershell
python 03_raw_to_rgb/01_raw_to_rgb_demo.py --image C:/path/to/image.png
```

调参数：

```powershell
python 03_raw_to_rgb/01_raw_to_rgb_demo.py --blue-gain 1.1 --green-gain 1.0 --red-gain 0.9 --gamma 0.8 --exposure 1.3
```

切换颜色校正矩阵风格：

```powershell
python 03_raw_to_rgb/01_raw_to_rgb_demo.py --color-style warm
python 03_raw_to_rgb/01_raw_to_rgb_demo.py --color-style cool
python 03_raw_to_rgb/01_raw_to_rgb_demo.py --color-style vivid
```

颜色校正矩阵练习：

```powershell
python 03_raw_to_rgb/02_color_correction_matrix.py
```

颜色校正矩阵手写练习：

```powershell
python 03_raw_to_rgb/03_color_matrix_practice.py
```

黑电平 / 白电平 / 归一化练习：

```powershell
python 03_raw_to_rgb/04_black_white_level_practice.py
```

曝光补偿 / 裁剪练习：

```powershell
python 03_raw_to_rgb/05_exposure_clipping_practice.py
python 03_raw_to_rgb/05_exposure_clipping_practice.py --gain 2.5
```

自动曝光挑战练习：

```powershell
python 03_raw_to_rgb/06_auto_exposure_practice.py
python 03_raw_to_rgb/06_auto_exposure_practice.py --target-mean 0.45 --max-gain 3.0
```

高光保护自动曝光练习：

```powershell
python 03_raw_to_rgb/07_highlight_protection_ae_practice.py
python 03_raw_to_rgb/07_highlight_protection_ae_practice.py --target-mean 0.85 --max-clipped-ratio 0.03
```

## 输出文件

```text
03_raw_to_rgb/outputs/01_raw_to_rgb_demo/
  01_input_bgr.png
  02_fake_bayer_raw.png
  03_demosaic_bgr.png
  04_white_balance.png
  05_color_corrected.png
  06_gamma.png
  07_tone_mapped.png
  compare.png

03_raw_to_rgb/outputs/02_color_correction_matrix/
  01_input.png
  02_identity.png
  03_warm.png
  04_cool.png
  05_vivid.png
  compare.png

03_raw_to_rgb/outputs/03_color_matrix_practice/
  01_input.png
  02_identity.png
  03_warm.png
  04_cool.png
  compare.png

03_raw_to_rgb/outputs/04_black_white_level_practice/
  01_input.png
  02_fake_12bit_raw_preview.png
  03_normalized_preview.png
  compare.png
  histogram.png

03_raw_to_rgb/outputs/05_exposure_clipping_practice/
  01_input.png
  02_before_exposure.png
  03_after_exposure.png
  compare.png
  histogram.png

03_raw_to_rgb/outputs/06_auto_exposure_practice/
  01_input.png
  02_before_exposure.png
  03_manual_exposure.png
  04_auto_exposure.png
  compare.png
  histogram.png

03_raw_to_rgb/outputs/07_highlight_protection_ae_practice/
  01_input.png
  02_before_exposure.png
  03_mean_auto_exposure.png
  04_highlight_safe_exposure.png
  compare.png
  histogram.png
```

## 这一阶段要练什么

- 能把一个完整流程写成一个脚本。
- 能用命令行参数调白平衡、gamma 和曝光。
- 能看懂颜色校正矩阵如何混合 B/G/R 三个通道。
- 能自己写出 `apply_color_matrix()` 的核心数组运算。
- 能理解黑电平、白电平和 RAW 归一化的关系。
- 能观察曝光补偿如何让图像变亮，以及为什么高光会裁剪。
- 能根据图像平均亮度计算简单自动曝光增益。
- 能用过曝比例约束自动曝光，保护高光细节。
- 能保存每一步中间结果。
- 能用 `compare.png` 讲清楚 RAW-to-RGB 的流程。

## 下一步

填写 `STAGE_REVIEW.md`，用自己的话复盘 RAW-to-RGB、颜色校正、曝光补偿和高光保护自动曝光。
