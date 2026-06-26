# -*- coding: utf-8 -*-
"""
PyTorch 图像学习第 5 课：保存和加载模型参数。

这一课只做一件事：
    训练一个很小的 TinyMLP，把参数保存到 checkpoint，再加载到新模型里。
"""

from pathlib import Path

import torch


script_dir = Path(__file__).resolve().parent
checkpoint_dir = script_dir / "checkpoints"
checkpoint_dir.mkdir(parents=True, exist_ok=True)
checkpoint_path = checkpoint_dir / "tiny_mlp_state_dict.pth"


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


def train_model(model, x, target, learning_rate, num_steps):
    """训练模型若干步，并返回最后一次 loss 数值。"""
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    loss_value = 0.0

    for _ in range(num_steps):
        output = model(x)
        loss = calculate_mse_loss(output, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        loss_value = loss.item()

    return loss_value


def save_model_state(model, save_path):
    """保存模型参数 state_dict。"""
    # TODO: 变量名建议：state_dict
    state_dict = model.state_dict()
    torch.save(state_dict,save_path)
 


def load_model_state(model, load_path):
    """从文件加载模型参数 state_dict。"""
    # TODO: 变量名建议：state_dict
    state_dict = torch.load(load_path)
    model.load_state_dict(state_dict)



def main():
    """运行第 5 课。"""
    torch.manual_seed(0)

    x, target = make_toy_data()

    model = TinyMLP(in_features=4, hidden_features=8, out_features=2)
    loss_value = train_model(model, x, target, learning_rate=0.1, num_steps=20)
    print("训练后 loss:", loss_value)

    save_model_state(model, checkpoint_path)
    loss_value = train_model(model, x, target, learning_rate=0.1, num_steps=20)
    print("训练后 loss:", loss_value)
    print("已保存模型参数:", checkpoint_path)

    new_model = TinyMLP(in_features=4, hidden_features=8, out_features=2)
    load_model_state(new_model, checkpoint_path)
    print("已加载模型参数到 new_model")

    old_output = model(x)
    new_output = new_model(x)
    max_diff = torch.max(torch.abs(old_output - new_output)).item()
    print("旧模型和新模型输出最大差异:", max_diff)


if __name__ == "__main__":
    main()
