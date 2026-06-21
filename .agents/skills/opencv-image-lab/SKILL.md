---
name: opencv-image-lab
description: Build beginner OpenCV image-processing exercises inside career_imaging_learning. Use when the user asks about reading images, BGR/RGB, grayscale conversion, histograms, blur, denoise, sharpen, noise, PSNR, before-after comparison, or scripts under 01_opencv_basic.
---

# OpenCV Image Lab

Use this skill for small OpenCV experiments that produce visible image outputs.

## Rules

- Keep scripts beginner-friendly and compatible with Python 3.8 syntax.
- Write Chinese comments explaining image arrays and processing steps.
- Avoid `cv2.imshow`; save images to `01_opencv_basic/outputs/<lesson_name>/`.
- If no input image is available, generate a simple demo image in code.
- Print image `shape`, `dtype`, and value range after major steps.
- Remember OpenCV reads color images as `BGR`, not `RGB`.

## Workflow

1. Choose one image-processing goal.
2. Create or edit one script under `01_opencv_basic/`.
3. Use `pathlib.Path` for paths.
4. Save original, processed image, and comparison or plot when useful.
5. Run the script and confirm output files exist.
6. Update or create the chapter README when the lesson needs a record.

## Common Lessons

- Read, print shape, save image.
- Convert BGR to RGB and grayscale.
- Draw grayscale histogram with Matplotlib.
- Apply Gaussian blur and mean blur.
- Add Gaussian noise and denoise.
- Sharpen with a simple convolution kernel.
- Compute PSNR for before-after comparison.

## Output Standard

Each lesson should leave artifacts the user can inspect:

```text
01_opencv_basic/outputs/<lesson_name>/
  original.png
  result.png
  comparison.png
```
