---
name: mini-isp-lab
description: Build a minimal ISP and RAW-to-RGB learning pipeline inside career_imaging_learning. Use when the user asks about Bayer patterns, fake RAW, RGGB, demosaic, white balance, color correction, gamma correction, tone mapping, or scripts under 02_mini_isp and 03_raw_to_rgb.
---

# Mini ISP Lab

Use this skill to teach ISP through a minimal, inspectable pipeline rather than industrial ISP complexity.

## Rules

- Keep physics and image-processing steps explicit.
- Prefer NumPy/OpenCV code that the user can read line by line.
- Use Chinese comments for Bayer, demosaic, white balance, gamma, and tone mapping.
- Save each pipeline stage as an image.
- Print array `shape`, `dtype`, `min`, `max`, and value range after important steps.
- Make clear when data is simulated from RGB rather than real camera RAW.

## Workflow

1. Start from a normal RGB/BGR image or generated demo image.
2. Simulate RGGB Bayer if real RAW is not available.
3. Implement one stage per script before combining into a pipeline.
4. Save intermediate results under `02_mini_isp/outputs/<lesson_name>/` or `03_raw_to_rgb/outputs/<lesson_name>/`.
5. Add a short README explanation for the pipeline stages.
6. Run a smoke check and confirm output images are created.

## Minimal Pipeline

Use this teaching order:

1. `RGB image -> fake RGGB Bayer`
2. `Bayer -> simple demosaic`
3. `white balance gain`
4. `color correction matrix` when needed
5. `gamma correction`
6. `tone mapping / clipping`
7. `save final RGB image`

## Interview Framing

Emphasize that RAW-to-RGB is a pipeline of array transformations. Demosaic fills missing color samples, white balance corrects channel gains, gamma changes display brightness, and tone mapping compresses intensity for viewing.
