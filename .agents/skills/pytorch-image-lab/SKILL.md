---
name: pytorch-image-lab
description: Build beginner PyTorch image-learning exercises inside career_imaging_learning. Use when the user asks about tensors, Dataset, DataLoader, nn.Module, loss, backward, optimizer.step, saving/loading models, tiny CNN denoising, image patches, PSNR, or scripts under 04_pytorch_image.
---

# PyTorch Image Lab

Use this skill to turn PyTorch concepts into tiny image experiments.

## Rules

- Keep models small enough to run on CPU.
- Keep code compatible with Python 3.8 syntax.
- Write Chinese comments for tensor shapes, model inputs/outputs, loss, and optimizer steps.
- Print tensor `shape`, `dtype`, device, and loss values.
- Avoid long training unless the user explicitly asks for it.
- Save loss curves and before-after images for every training demo.

## Workflow

1. Start with tensor shape or a tiny model before training a CNN.
2. Create or edit one script under `04_pytorch_image/`.
3. Use small synthetic or generated image data when no dataset is available.
4. Train for a small number of epochs by default.
5. Save checkpoints under `04_pytorch_image/checkpoints/`.
6. Save outputs under `04_pytorch_image/outputs/<lesson_name>/`.
7. Verify by importing `torch` and running one forward pass or a tiny training loop.

## Teaching Order

- `01_tensor_shape.py`: tensor creation, reshape, channel order.
- `02_linear_model.py`: linear layer and output shape.
- `03_tiny_mlp.py`: small network and loss.
- `04_save_load_model.py`: checkpoint save/load.
- `05_make_noisy_dataset.py`: noisy-clean image pairs.
- `06_tiny_denoise_cnn.py`: small `Conv-ReLU-Conv-ReLU-Conv` model.
- `07_train_denoise.py`: MSE training loop.
- `08_eval_denoise.py`: before-after image and PSNR.

## Shape Convention

Use PyTorch image tensors as `N, C, H, W`. Explain this every time it appears until the user is comfortable.
