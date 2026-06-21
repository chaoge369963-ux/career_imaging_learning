---
name: debug-shape-traceback
description: Debug beginner Python, NumPy, OpenCV, and PyTorch errors in career_imaging_learning. Use when the user pastes a traceback, shape mismatch, dtype error, path error, OpenCV read failure, Matplotlib save issue, PyTorch tensor dimension error, or asks why a script does not run.
---

# Debug Shape Traceback

Use this skill for runtime-grounded debugging. Reproduce the failure before explaining whenever possible.

## Rules

- Read the exact traceback and identify the first user-code line that failed.
- Do not guess from symptoms if the script can be run locally.
- Add temporary print statements only when needed; remove noisy debug prints unless they are useful for learning.
- Preserve beginner readability and Chinese comments.
- For image/tensor problems, inspect `shape`, `dtype`, `min`, `max`, and path existence.

## Workflow

1. Reproduce the command or infer the likely command from the script.
2. Locate the failing file and line.
3. Check path existence before changing image-loading logic.
4. Check array/tensor shape before changing model or OpenCV code.
5. Patch the smallest necessary change.
6. Rerun the failing command.
7. Explain the root cause in plain Chinese.

## Common Checks

- `cv2.imread(...) is None`: path wrong, unsupported file, or non-ASCII path issue.
- OpenCV color error: grayscale image passed where BGR was expected.
- Matplotlib backend issue: use `matplotlib.use("Agg")` before importing `pyplot`.
- NumPy broadcasting error: compare both operand shapes.
- PyTorch channel error: expected `N, C, H, W`, got `H, W, C` or missing batch dimension.
- Windows `conda run` Unicode error: run the environment `python.exe` directly.

## Response Style

Lead with the concrete failing line and fix. Then explain the concept briefly so the user learns the pattern for next time.
