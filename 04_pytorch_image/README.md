# 04_pytorch_image

这一阶段开始学习 PyTorch 图像处理基础。

目标不是一上来训练大模型，而是先看懂图像在 PyTorch 里的形状变化。

## 第 1 课：Tensor Shape

脚本：

```text
01_tensor_shape.py
```

运行命令：

```powershell
python 04_pytorch_image/01_tensor_shape.py
```

这一课要理解：

```text
NumPy 图像常见形状：H, W, C
PyTorch 图像常见形状：C, H, W
PyTorch 模型输入常见形状：N, C, H, W
H = 高度
W = 宽度
C = 通道数
N = batch 数量
```

## 本课 TODO

请你完成 `01_tensor_shape.py` 里的 3 个函数：

```text
to_float01()
hwc_to_chw_tensor()
add_batch_dim()
```

完成后要能解释：

```text
为什么图像要除以 255
为什么 H,W,C 要变成 C,H,W
为什么模型输入前面要多一个 N
```

## 第 2 课：Linear Model

脚本：

```text
02_linear_model.py
```

运行命令：

```powershell
python 04_pytorch_image/02_linear_model.py
```

这一课要理解：

```text
N,C,H,W 是一批图像
N,F 是把每张图展平成一行特征
nn.Linear(in_features, out_features) 会把 F 个输入数变成 out_features 个输出数
```

## 本课 TODO

请你完成 `02_linear_model.py` 里的 3 个函数：

```text
flatten_image_batch()
build_linear_model()
run_model()
```

## 第 3 课：Tiny MLP

脚本：

```text
03_tiny_mlp.py
```

运行命令：

```powershell
python 04_pytorch_image/03_tiny_mlp.py
```

这一课要理解：

```text
nn.Module：自己定义模型时要继承的基类
__init__：放模型有哪些层
forward：放数据怎么流过这些层
loss：衡量 output 和 target 差多少
```

## 本课 TODO

请你完成 `03_tiny_mlp.py` 里的 3 个部分：

```text
TinyMLP.__init__()
TinyMLP.forward()
calculate_mse_loss()
```

## 第 4 课：Train Tiny MLP

脚本：

```text
04_train_tiny_mlp.py
```

运行命令：

```powershell
python 04_pytorch_image/04_train_tiny_mlp.py
```

这一课要理解：

```text
optimizer.zero_grad()：清空旧梯度
loss.backward()：根据 loss 计算梯度
optimizer.step()：根据梯度更新模型参数
loss 下降：说明模型输出正在接近 target
```

## 本课 TODO

请你完成 `04_train_tiny_mlp.py` 里的 2 个函数：

```text
build_optimizer()
train_one_step()
```

## 第 5 课：Save / Load Model

脚本：

```text
05_save_load_model.py
```

运行命令：

```powershell
python 04_pytorch_image/05_save_load_model.py
```

这一课要理解：

```text
state_dict：模型参数字典，里面保存 weight 和 bias
torch.save()：把参数保存到文件
torch.load()：从文件读取参数
load_state_dict()：把参数装回模型
```

输出文件：

```text
04_pytorch_image/checkpoints/tiny_mlp_state_dict.pth
```

## 本课 TODO

请你完成 `05_save_load_model.py` 里的 2 个函数：

```text
save_model_state()
load_model_state()
```

## 第 6 课：Make Noisy Dataset

脚本：

```text
06_make_noisy_dataset.py
```

运行命令：

```powershell
python 04_pytorch_image/06_make_noisy_dataset.py
```

这一课要理解：

```text
Dataset：定义数据从哪里来
__len__：数据集有多少个样本
__getitem__：按 index 取一个样本
DataLoader：把多个样本打包成 batch
noisy-clean pair：图像去噪训练时的输入和目标
```

输出文件：

```text
04_pytorch_image/outputs/06_make_noisy_dataset/clean_noisy_compare.png
```

## 本课 TODO

请你完成 `06_make_noisy_dataset.py` 里的 4 个部分：

```text
rgb_uint8_to_tensor_chw()
add_noise_to_tensor()
NoisyCleanDataset.__len__()
NoisyCleanDataset.__getitem__()
```
