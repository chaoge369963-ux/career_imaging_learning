# -*- coding: utf-8 -*-
"""
PyTorch 图像学习第 3 课：Tiny MLP 和 loss。

这一课只做一件事：
    自己写一个继承 torch.nn.Module 的小模型，并计算一次 MSE loss。
"""

import torch


def make_toy_data():
    """生成一组很小的输入和目标输出。"""
    x = torch.tensor(
        [
            [0.0, 0.0, 1.0, 1.0],
            [1.0, 0.0, 0.0, 1.0],
            [0.2, 0.8, 0.2, 0.8],
        ],
        dtype=torch.float32,
    )
    target = torch.tensor(
        [
            [0.0, 1.0],
            [1.0, 0.0],
            [0.5, 0.5],
        ],
        dtype=torch.float32,
    )
    return x, target


class TinyMLP(torch.nn.Module):
    """一个很小的多层感知机。"""

    def __init__(self, in_features, hidden_features, out_features):
        """定义模型里有哪些层。"""
        super().__init__()
        # TODO: 变量名建议：self.linear1, self.relu, self.linear2
        self.linear1 = torch.nn.Linear(in_features, hidden_features)
        self.linear2 = torch.nn.Linear(hidden_features, hidden_features)
        self.relu = torch.nn.ReLU()
        self.linear3 = torch.nn.Linear(hidden_features, out_features)

    def forward(self, x):
        """定义数据怎么从输入流到输出。"""
        # TODO: 变量名建议：hidden, output
        hidden = self.linear1(x)
        hidden = self.relu(hidden)
        hidden = self.linear2(hidden)
        hidden = self.relu(hidden)
        output = self.linear3(hidden)
        return output


def calculate_mse_loss(output, target):
    """计算 output 和 target 的均方误差。"""
    # TODO: 变量名建议：loss_fn, loss
    loss_fn = torch.nn.MSELoss()
    loss = loss_fn(output, target)
    return loss


def print_tensor_info(name, tensor):
    """打印 tensor 的 shape 和 dtype。"""
    print(name)
    print("  shape:", tensor.shape)
    print("  dtype:", tensor.dtype)
    print("  value:")
    print(tensor)


def main():
    """运行第 3 课。"""
    torch.manual_seed(0)

    x, target = make_toy_data()
    print_tensor_info("1. 输入 x: N,F", x)
    print_tensor_info("2. 目标 target: N,out_features", target)

    model = TinyMLP(in_features=4, hidden_features=8, out_features=2)
    print("3. 模型结构：")
    print(model)

    output = model(x)
    print_tensor_info("4. 模型输出 output", output)

    loss = calculate_mse_loss(output, target)
    print("5. MSE loss:", float(loss.detach()))


if __name__ == "__main__":
    main()
