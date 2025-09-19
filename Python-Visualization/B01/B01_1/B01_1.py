# -*- coding: utf-8 -*-
# @Time    : 2025/9/19 19:16
# @Author  : AndyChen
# @FileName: B01_1.py
# @Software: PyCharm

# 基本散点图

## 1. 导入必要库并配置样式

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
from cycler import cycler

colors = ["#fe8383"]
plt.rcParams.update(
    {
        # 设置中文字体，以正常显示中文
        "font.sans-serif": ["Microsoft YaHei"],
        "axes.unicode_minus": False,
        # 自定义样式
        "figure.figsize": (8, 5),
        "figure.dpi": 100,
        "axes.prop_cycle": cycler(color=colors),
        "axes.facecolor": "#fefaf9",
        "axes.edgecolor": "#ffffff",
        "axes.titleweight": "bold",
        "axes.titlecolor": "#e16259",
        "axes.labelweight": "bold",
        "axes.labelcolor": "#e16259",
        "xtick.color": "#e16259",
        "ytick.color": "#e16259",
    }
)

## 2. 准备数据

# 从文件中读取数据
data = pd.read_csv("data.csv")
X = data["X"]
Y = data["Y"]

## 3. 创建窗口并绘制主图

fig, ax = plt.subplots()
# 绘制散点
ax.scatter(X, Y, s=100, c=colors[0], alpha=0.5)
# 绘制投影
ax.scatter(X, [0] * len(X), marker="|", c=colors[0], alpha=0.5, s=300)
ax.scatter([0] * len(X), Y, marker="_", c=colors[0], alpha=0.5, s=300)

## 4. 添加辅助元素

# 设置刻度间距
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))

# 设置文本信息
ax.set_title("基本散点图")
ax.set_xlabel("X轴")
ax.set_ylabel("Y轴")

plt.tight_layout()
plt.show()
