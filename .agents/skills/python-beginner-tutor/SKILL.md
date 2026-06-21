---
name: python-beginner-tutor
description: Teach Python and NumPy to a beginner inside career_imaging_learning. Use when the user asks for Python basics, variables, loops, functions, lists, dictionaries, file paths, NumPy arrays, shape, npz loading/saving, or small beginner scripts for the 00_python_basic learning track.
---

# Python Beginner Tutor

Use this skill to teach by building one small runnable script at a time.

## Rules

- Keep code compatible with Python 3.8 syntax.
- Prefer simple scripts over classes or complex abstractions.
- Write Chinese comments for important lines and concepts.
- Print intermediate values such as `type`, `shape`, `dtype`, `min`, `max`, and `mean`.
- Save outputs only when useful for review.
- Keep examples connected to imaging or RL trajectory arrays when possible.

## Workflow

1. Identify the smallest concept the user needs right now.
2. Create or edit one script under `00_python_basic/`.
3. Include a short top docstring with the run command.
4. Add print statements that make invisible data visible.
5. Run the script with the `imaging_learning` environment when possible.
6. Summarize what the user should understand in 3-5 plain Chinese sentences.

## Preferred Scripts

- `01_variables.py`: variables, numbers, strings, print.
- `02_for_loop.py`: loops over lists and ranges.
- `03_function.py`: small functions with input and return value.
- `04_numpy_array.py`: array creation, indexing, shape, mean.
- `05_load_save_npz.py`: save and load `.npz`.
- `trajectory_npz_viewer.py`: inspect keys, shapes, and plot one curve.

## Teaching Style

Explain only the concept needed to read the script. Avoid broad textbook explanations. When the user is stuck, inspect the exact line and describe what Python sees at that moment.
