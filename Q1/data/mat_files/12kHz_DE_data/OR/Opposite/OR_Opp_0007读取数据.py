# -*- coding: utf-8 -*-
# @Time    : 2025/9/21 14:32
# @Author  : AndyChen
# @FileName: OR_Opp_0007读取数据.py
# @Software: PyCharm

import scipy.io as sio
import pandas as pd
import os

# 存放 .mat 文件的文件夹路径
mat_folder = "./0007"
# 输出文件夹
output_folder = "./数据/0007"
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹下所有的 .mat 文件
for file in os.listdir(mat_folder):
    if file.endswith(".mat"):
        file_path = os.path.join(mat_folder, file)
        # 读取 .mat 文件
        mat_data = sio.loadmat(file_path)

        # 删除mat文件中默认的元信息（__header__, __version__, __globals__）
        clean_data = {k: v for k, v in mat_data.items() if not k.startswith("__")}

        # 生成一个 Excel 文件名
        excel_name = os.path.splitext(file)[0] + ".xlsx"
        excel_path = os.path.join(output_folder, excel_name)

        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            for var_name, var_data in clean_data.items():
                try:
                    # 转换为 DataFrame
                    df = pd.DataFrame(var_data)
                except Exception as e:
                    print(f"变量 {var_name} 在文件 {file} 中不能转换为 DataFrame: {e}")
                    continue

                # 写入 Excel，每个变量一个 sheet
                sheet_name = var_name[:30]  # Excel 限制 sheet 名 <=31 字符
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"{file} 已保存到 {excel_path}")

print("所有 .mat 文件已处理完成！")