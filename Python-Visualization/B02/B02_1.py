# -*- coding: utf-8 -*-
# @Time    : 2025/9/19 19:51
# @Author  : AndyChen
# @FileName: B02_1.py
# @Software: PyCharm

"""使用 matplotlib 绘制堆叠面积图"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from scipy.interpolate import make_interp_spline
import random
from scipy.signal import find_peaks


def load_style():
    """加载样式"""
    try:
        plt.style.use("chartlab.mplstyle")
    except:
        pass
    # 设置中文字体，以正常显示中文
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["grid.color"] = "#fed2d2"


def create_data(x, size, n, max_value):
    """通过高斯函数生成一组平滑数据"""
    sigma = size / 30  # 控制平滑度
    values = max_value * np.exp(-0.5 * ((x - n) / sigma) ** 2)
    return values


def create_stacked_area_chart(ax):
    """创建堆叠面积图"""

    ## 1.生成随机数据
    random.seed(64)
    categories = []  # 数据标签
    size = 300
    x_max = 80
    x = np.linspace(0, x_max, size)
    peaks = [5, 15, 23, 30, 35, 40, 53, 60]
    means = [2.5, 1.2, 3.0, 2.5, 1.0, 1.5, 2.0, 2.2]
    y_list = []
    for i in range(8):
        temp_y = 0
        categories.append(f"类别{i+1}")
        for j in range(len(peaks)):
            temp_y += create_data(x, x_max, peaks[j], means[j] * random.random())
        y_list.append(temp_y)

    # 配色表
    colors = [
        "#214e81",
        "#456991",
        "#6983a2",
        "#8d9eb2",
        "#b59fb1",
        "#dc9fb0",
        "#cf8b9e",
        "#c2768b",
    ]
    ## 2.绘制图像
    # 绘制堆叠面积图
    ax.stackplot(x, y_list, colors=colors, labels=categories, zorder=10, alpha=1)
    # 绘制分割线
    y_stack = np.cumsum(y_list, axis=0)
    for i in range(len(y_list)):
        ax.plot(x, y_stack[i], color="#ffffff", zorder=20, linewidth=1)
    index, _ = find_peaks(y_stack[-1])
    # 绘制最大数据折线
    ax.plot(
        x[index],
        y_stack[-1][index],
        color=colors[-1],
        zorder=20,
        linewidth=1,
        linestyle=":",
        marker="o",
        markerfacecolor="#ffffff",
    )
    # 添加数据标签
    x_offset = [0, -1, 0, 1, 0, 0, 0.5]  # 数据标签的x方向偏移值
    for i in range(len(x[index])):
        ax.text(
            x[index][i] + x_offset[i],
            y_stack[-1][index][i] + 0.2,
            f"{y_stack[-1][i]:.2f}",
            ha="center",
            va="bottom",
            color=colors[-1],
            zorder=30,
            fontweight="bold",
        )

    ax.set_title("堆叠面积图")  # 图像标题
    ax.set_xlabel("X轴")  # X轴标签
    ax.set_ylabel("数值")  # Y轴标签
    ax.set_xlim(0, 70)  # 轴范围
    ax.set_ylim(0, 18)
    ax.legend(loc="upper center", ncol=4, prop={"weight": "bold"})  # 图例

    # 绘制网格
    ax.minorticks_on()
    ax.grid(axis="y", which="major", linestyle="-", linewidth="0.5")
    ax.grid(axis="y", which="minor", linestyle=":", linewidth="0.5")
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))  # 主网格间距
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))  # 次网格间距

    plt.tight_layout()


if __name__ == "__main__":
    load_style()
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    create_stacked_area_chart(ax)
    plt.show()