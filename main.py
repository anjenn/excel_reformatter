import tkinter as tk
import pandas as pd
import os
from tkinter import StringVar, font, ttk
# -*- coding: utf-8 -*-
from openpyxl import load_workbook, Workbook
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 윈도우 기본 한글 폰트 설정 (예: 'Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


# 경로 설정

root_folder = os.getcwd()  # 현재 작업 디렉토리
input_file = os.path.join(root_folder, "csv", "매출합계표_05_19.xlsx")  # 더미 엑셀 파일 경로
output_folder = os.path.join(root_folder, "output")  # 아웃풋 폴더 경로
OUTPUT_FILENAME = "reformatted.xlsx"


# 아웃풋 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def load_excel_data(file_path):
    # 엑셀 파일 읽기
    try:
        df = pd.read_excel(input_file, engine='openpyxl')  # 엑셀 파일 읽기
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_file}")
        exit()

    # headers_dict = {header: idx for idx, header in enumerate(df.columns)}

    headers_dict = {
        col: idx for idx, col in enumerate(df.columns)
        if df[col].iloc[1:].notna().any()  # 첫 행 제외한 나머지 행에 데이터가 하나라도 있으면 포함
    }
    print("헤더 인덱스:", headers_dict)

    # dropdown_list = df.columns.tolist()
    dropdown_list = list(headers_dict.keys())
    print("드롭다운 리스트:", dropdown_list)

    return df, headers_dict, dropdown_list

def convert_to_datetime(df, headers_dict):
    col = '일자'
    if col in headers_dict:
        idx = headers_dict[col]
        # 데이터프레임의 해당 열을 datetime으로 변환
        df.iloc[:, idx] = pd.to_datetime(df.iloc[:, idx], errors='coerce')
    return df

def create_plot(df, headers_dict, selected_option1, selected_option2):
    df = df.iloc[:-1]
    df = convert_to_datetime(df, headers_dict)

    selected_value1 = selected_option1.get()
    selected_value2 = selected_option2.get()

    # 선택된 값에 따라 데이터 처리
    if selected_value1 in headers_dict and selected_value2 in headers_dict:

        col_idx1 = headers_dict[selected_value1]
        col_idx2 = headers_dict[selected_value2]
        
        x = df.iloc[:, col_idx1]
        y = df.iloc[:, col_idx2]

        x = pd.to_numeric(x, errors='coerce')
        y = pd.to_numeric(y, errors='coerce')

        mask = x.notna() & y.notna()
        x = x[mask]
        y = y[mask]
                        
        plt.scatter(x, y, label='데이터')

        # Trend line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), 'r-', label='추세선')
        
        plt.xlabel(df.columns[col_idx1])
        plt.ylabel(df.columns[col_idx2])
        plt.title("산점도")

        plt.grid(True)
        plt.legend()
        plt.show()

    else:
        print("잘못된 선택입니다.")


######################################################################
######################################################################
######################################################################

# 프로그램 인터페이스
df, headers_dict, dropdown_list = load_excel_data(input_file)

root = tk.Tk()
custom_font = font.Font(family="Malgun Gothic", size=12)
root.geometry("300x200")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.title("Excel Data Manipulation")

def show_widgets(dropdown_list, trigger_button):
    trigger_button.grid_remove()
    
    # Title
    title_label = ttk.Label(root, text="옵션을 선택하세요", font=("Arial", 14))
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))


    label1 = ttk.Label(root, text="항목 1:")
    label1.grid(row=1, column=0, sticky='e', padx=(10, 5), pady=5)
    options1 = dropdown_list

    selected_option1 = tk.StringVar(value=options1[0])
    dropdown1 = ttk.OptionMenu(root, selected_option1, selected_option1.get(), *options1)
    dropdown1.grid(row=1, column=1, sticky='w', padx=(5, 10), pady=5)


    label2 = ttk.Label(root, text="항목 2:")
    label2.grid(row=2, column=0, sticky='e', padx=(10, 5), pady=5)
    options2 = dropdown_list

    selected_option2 = tk.StringVar(value=options2[0])
    dropdown2 = ttk.OptionMenu(root, selected_option2, selected_option2.get(), *options2)
    dropdown2.grid(row=2, column=1, sticky='w', padx=(5, 10), pady=5)


    submit_button = tk.Button(root, text="선택 완료", command=lambda: create_plot(df, headers_dict, selected_option1, selected_option2), font=custom_font)
    submit_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

        # 숨김 버튼 제거 (한 번만 누르게)
    show_button.grid_remove()


# # 처음 보여지는 버튼
show_button = ttk.Button(root, text="시작하기", command=lambda: show_widgets(dropdown_list, show_button), style='TButton')
show_button.grid(row=0, column=0, columnspan=2, pady=50)
root.mainloop()
