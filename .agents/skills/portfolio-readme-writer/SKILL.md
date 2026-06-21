---
name: portfolio-readme-writer
description: Write portfolio-quality README files and learning notes for career_imaging_learning projects. Use when the user asks to summarize a project, write a README, organize outputs, prepare resume bullets, explain mini ISP, AI denoising, RL-SNN3 trajectory analysis, or turn experiments into interview-ready project descriptions.
---

# Portfolio README Writer

Use this skill to turn learning scripts into project artifacts the user can show.

## Rules

- Write in clear Chinese by default unless the user asks for English.
- Keep claims honest: describe what the code actually does, not what a full industry system would do.
- Include run commands and output paths.
- Mention screenshots or result images only when they exist.
- Keep README practical: goal, input, method, output, result, learning, next step.
- Do not modify `RL_SNN3` code unless explicitly requested.

## README Structure

Use this structure for project README files:

```markdown
# Project Name

## 项目目标

## 输入输出

## 核心流程

## 运行命令

## 结果文件

## 我学到了什么

## 下一步改进
```

## Resume Bullet Style

Use concise action-result wording:

```text
实现 mini ISP pipeline，包括 Bayer 模拟、简单 demosaic、白平衡、gamma correction 和 tone mapping；使用 OpenCV/NumPy 完成图像处理流程，并输出各阶段可视化结果。
```

## Teaching Notes

For weekly notes, use:

```markdown
# 第 X 周复盘

## 完成了什么

## 哪里没懂

## 代码能不能跑

## 下周目标
```
