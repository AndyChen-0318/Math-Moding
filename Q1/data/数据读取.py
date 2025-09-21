# -*- coding: utf-8 -*-
# @Time    : 2025/9/21 14:46
# @Author  : AndyChen
# @FileName: 数据读取.py
# @Software: PyCharm

import os
import numpy as np
import pandas as pd
import scipy.io as sio

# ======== 你可以改这里 ========
src_root = "./mat_files"   # 放.mat文件的根目录
dst_root = "./数据"       # 输出Excel的根目录（将按原层级镜像）
# ============================

def var_to_dataframe(var_name, var_value):
    """
    尝试把不同类型的MAT变量转成DataFrame：
    - 2D数组：直接转
    - 1D数组：转成单列
    - 3D+/不规则：拉平成二维
    - 结构化数组/dict：按字段展开为列（尽力）
    转换不了就返回None
    """
    try:
        # 结构/字典
        if isinstance(var_value, dict):
            flat = {}
            for k, v in var_value.items():
                arr = np.array(v)
                if arr.ndim == 0:
                    flat[k] = [arr.item()]
                elif arr.ndim == 1:
                    flat[k] = arr
                else:
                    flat[k] = arr.reshape(arr.shape[0], -1) if arr.shape[0] > 1 else arr.reshape(-1)
            return pd.DataFrame(flat)

        arr = np.array(var_value)

        # 结构化dtype（类似表）
        if arr.dtype.names:
            cols = {name: np.array(arr[name]).reshape(-1) for name in arr.dtype.names}
            return pd.DataFrame(cols)

        # 对象/cell类型：尽力拉直
        if arr.dtype == object:
            # squeeze后列表化
            squeezed = np.squeeze(arr)
            # 如果是一维的对象数组，直接成一列
            if squeezed.ndim == 1:
                return pd.DataFrame({var_name: squeezed})
            # 二维对象数组：逐列转字符串表示（避免失败）
            if squeezed.ndim == 2:
                ncols = squeezed.shape[1]
                data = {f"{var_name}_{i}": squeezed[:, i] for i in range(ncols)}
                return pd.DataFrame(data)
            # 其它维度：转成一列字符串
            return pd.DataFrame({var_name: [squeezed]})

        # 数值/布尔/字符串数组
        if arr.ndim == 0:
            return pd.DataFrame({var_name: [arr.item()]})
        if arr.ndim == 1:
            return pd.DataFrame({var_name: arr})
        if arr.ndim == 2:
            return pd.DataFrame(arr)
        # 3D及以上：拉平成二维（以第一维为行）
        flat = arr.reshape(arr.shape[0], -1)
        cols = [f"{var_name}_{i}" for i in range(flat.shape[1])]
        return pd.DataFrame(flat, columns=cols)

    except Exception:
        return None

def save_mat_to_excel(mat_path, xlsx_path):
    # 读取 .mat；使用 squeeze_me / struct_as_record=False 让结构更扁平些
    mat = sio.loadmat(mat_path, squeeze_me=True, struct_as_record=False)
    # 去掉内部元信息
    data = {k: v for k, v in mat.items() if not k.startswith("__")}

    if not data:
        print(f"[跳过] {mat_path} 没有可导出的变量")
        return

    os.makedirs(os.path.dirname(xlsx_path), exist_ok=True)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        wrote_any = False
        for var_name, var_value in data.items():
            df = var_to_dataframe(var_name, var_value)
            if df is None:
                print(f"[提示] {os.path.basename(mat_path)} 的变量 {var_name} 暂无法转换为表，已跳过")
                continue
            # Excel工作表名限制31字符
            sheet_name = str(var_name)[:31] if str(var_name) else "Sheet1"
            # 索引一般无意义，默认不写
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            wrote_any = True

        if wrote_any:
            print(f"[完成] 已导出：{xlsx_path}")
        else:
            print(f"[跳过] {mat_path} 所有变量都无法转换为表")

def mirror_path_under_dst(src_file):
    """
    把 src_root 下的 src_file 路径镜像到 dst_root，
    并把扩展名改为 .xlsx
    """
    rel_dir = os.path.relpath(os.path.dirname(src_file), start=src_root)
    base = os.path.splitext(os.path.basename(src_file))[0] + ".xlsx"
    return os.path.join(dst_root, rel_dir, base)

def main():
    count = 0
    for root, _, files in os.walk(src_root):
        for fname in files:
            if fname.lower().endswith(".mat"):
                src_path = os.path.join(root, fname)
                dst_path = mirror_path_under_dst(src_path)
                save_mat_to_excel(src_path, dst_path)
                count += 1
    print(f"\n== 全部完成：共处理 {count} 个 .mat 文件，输出目录：{os.path.abspath(dst_root)} ==")

if __name__ == "__main__":
    main()
