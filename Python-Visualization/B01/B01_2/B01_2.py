# -*- coding: utf-8 -*-
# @Time    : 2025/9/19 19:53
# @Author  : AndyChen
# @FileName: B01_2.py
# @Software: PyCharm

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# =========================
# 用户配置
# =========================
read_custom_data = False  # 是否读取自定义数据（True 从 data.csv 读；False 生成内置 iris 并保存）

# =========================
# 读取数据
# =========================
if read_custom_data:
    iris = pd.read_csv("data.csv")
else:
    iris = sns.load_dataset("iris").rename(columns={
        "sepal_length": "Sepal.Length",
        "sepal_width": "Sepal.Width",
        "petal_length": "Petal.Length",
        "petal_width": "Petal.Width",
        "species": "Species"
    })
    # 可选：将生成的数据写出，便于下次直接读取
    try:
        iris.to_csv("data.csv", index=False)
    except Exception:
        pass

# 2) 配色：红(setosa)、蓝(versicolor)、黄(virginica)
palette = {"setosa": "#c0627a", "versicolor": "#5595d1", "virginica": "#e3b269"}
hue_order = ["setosa", "versicolor", "virginica"]

def _p_stars(p):
    if p < 1e-3:
        return "***"
    if p < 1e-2:
        return "**"
    if p < 5e-2:
        return "*"
    return ""

# 3) 上三角：总相关 + 分物种相关（含星标）
def corrpanel(x, y, **kws):
    ax = plt.gca()
    if hasattr(ax, "_corr_drawn"):
        return

    col_x = getattr(x, "name", None)
    col_y = getattr(y, "name", None)

    if not col_x or not col_y:
        ax.text(0.5, 0.5, "N/A", ha="center", va="center",
                transform=ax.transAxes, fontsize=12, fontweight="bold")
        ax._corr_drawn = True
        return

    r_all, p_all = pearsonr(iris[col_x], iris[col_y])
    txt_all = f"Corr: {r_all:+.3f}{_p_stars(p_all)}"

    lines = []
    for sp in hue_order:
        sub = iris[iris["Species"] == sp]
        r_sp, p_sp = pearsonr(sub[col_x], sub[col_y])
        lines.append((sp, r_sp, _p_stars(p_sp)))

    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.text(0.5, 0.80, txt_all, ha="center", va="center",
            transform=ax.transAxes, fontsize=12, fontweight="bold", color="#c0627a")

    y0 = 0.55
    dy = 0.18
    for i, (sp, r_sp, stars) in enumerate(lines):
        color = palette[sp]
        ax.text(0.5, y0 - i * dy, f"{sp}: {r_sp:+.3f}{stars}",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=11, color=color)

    ax._corr_drawn = True

# 4) 构建 PairGrid
vars_order = ["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"]
g = sns.PairGrid(
    iris,
    vars=vars_order,
    hue="Species",
    hue_order=hue_order,
    palette=palette,
    corner=False,
    diag_sharey=False
)

# 下三角：按物种分别拟合回归线并绘制散点
g.map_lower(
    sns.regplot,
    scatter_kws={"s": 25, "alpha": 0.5},
    line_kws={"lw": 1.5, "alpha": 0.9},
    ci=None
)

# 上三角：显示总相关 + 分物种相关
g.map_upper(corrpanel)

# 对角线：分物种直方图（白色边线）
g.map_diag(
    sns.histplot,
    common_norm=False,
    element="bars",
    alpha=0.55,
    bins=15,
    edgecolor="white",
    linewidth=1.0
)

# 5) 统一把轴线/刻度/标签设为深红
DARK_RED = "#c0627a"
for ax in g.axes.flatten():
    if ax is None:
        continue
    for spine in ax.spines.values():
        spine.set_color(DARK_RED)
        spine.set_linewidth(1.2)
    ax.tick_params(axis="both", colors=DARK_RED, which="both", width=1.0, labelcolor=DARK_RED)
    ax.xaxis.label.set_color(DARK_RED)
    ax.yaxis.label.set_color(DARK_RED)

# 图例与整体布局
g.add_legend(title="Species", ncols=3, bbox_to_anchor=(0.5, 0.98), loc="upper center")
leg = g._legend
if leg is not None:
    leg.get_title().set_color("#c0627a")
    for text in leg.get_texts():
        text.set_color("#c0627a")

g.figure.subplots_adjust(right=0.98, top=0.92, left=0.08, bottom=0.07)
g.figure.set_size_inches(8, 7)
g.figure.set_dpi(150)

plt.savefig("B01_2.png")

plt.show()
