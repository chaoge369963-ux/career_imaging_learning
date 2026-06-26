# -*- coding: utf-8 -*-
"""
PyTorch 图像学习第 4 课：backward 和 optimizer.step。

这一课只做一件事：
    让 TinyMLP 根据 loss 更新参数，观察 loss 是否下降。
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
        self.linear1 = torch.nn.Linear(in_features, hidden_features)
        self.relu = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(hidden_features, out_features)

    def forward(self, x):
        """定义数据怎么从输入流到输出。"""
        hidden = self.linear1(x)
        hidden = self.relu(hidden)
        output = self.linear2(hidden)
        return output


def calculate_mse_loss(output, target):
    """计算 output 和 target 的均方误差。"""
    loss_fn = torch.nn.MSELoss()
    loss = loss_fn(output, target)
    return loss


def build_optimizer(model, learning_rate):
    """创建优化器，用来更新模型参数。"""
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    return optimizer
  


def train_one_step(model, optimizer, x, target):
    """训练一步：前向、算 loss、反向传播、更新参数。"""
    output = model(x)
    loss = calculate_mse_loss(output, target)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item()


def main():
    """运行第 4 课。"""
    torch.manual_seed(0)

    x, target = make_toy_data()
    model = TinyMLP(in_features=4, hidden_features=8, out_features=2)
    optimizer = build_optimizer(model, learning_rate=0.1)

    print("模型开始训练。")
    for step in range(10):
        loss = train_one_step(model, optimizer, x, target)
        print("step:", step, "loss:", float(loss))


if __name__ == "__main__":
    main()
