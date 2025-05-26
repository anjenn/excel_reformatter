import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# 윈도우 기본 한글 폰트 설정 (예: 'Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
ROOT_DIR = os.getcwd()  # 현재 작업 디렉토리


def load_sales_data(input_file):
    # 엑셀 파일 읽기
    try:
        df = pd.read_excel(input_file, engine='openpyxl')  # 엑셀 파일 읽기
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_file}")
        exit()

    headers_dict = {}

    for idx, col in enumerate(df.columns):
        series = df[col].iloc[1:]  # Exclude first row

        if not df[col].iloc[1:].notna().any():
            print(f"Skipping column '{col}' due to empty cells.")
            continue

        # Check for consistent data types
        types = series.map(type).unique()
        if len(types) == 1:
            headers_dict[col] = idx

    dropdown_list = list(headers_dict.keys())

    return df, headers_dict, dropdown_list

def create_st_plot(df, headers_dict, opt1, opt2):
    plt.cla()
    df = df.iloc[:-1] # 마지막 행 제거

    selected1 = opt1.get()
    selected2 = opt2.get()

    if selected1 in headers_dict and selected2 in headers_dict:

        col_idx1 = headers_dict[selected1]
        col_idx2 = headers_dict[selected2]
        
        x = pd.to_numeric(df.iloc[:, col_idx1], errors='coerce')
        y = pd.to_numeric(df.iloc[:, col_idx2], errors='coerce')

        x = x[x.notna() & y.notna()] # NaN 값 제거 mask 적용
        y = y[x.notna() & y.notna()]
                        
        plt.scatter(x, y, label='데이터')

        # Trend line
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), 'r-', label='추세선')
        
        plt.xlabel(df.columns[col_idx1])
        plt.ylabel(df.columns[col_idx2])
        plt.title(f'{df.columns[col_idx1]} vs {df.columns[col_idx2]}')

        plt.grid(True)
        plt.legend()
        plt.show()

    else:
        print("잘못된 선택입니다.")

def create_lt_plot(combined_df, headers_dict, opt):
    plt.cla()
    selected = opt.get()
    x = 'Month'            # X-axis: date (from combined_df)
    y = selected          # Y-axis: selected column from dropdown
    plot_df = combined_df[[x, y]].copy()
    plot_df[y] = pd.to_numeric(plot_df[y], errors='coerce')
    plot_df = plot_df.dropna(subset=[x, y])

    if selected in headers_dict and not plot_df.empty:
        plot_df = plot_df.sort_values(by='Month')

        x_vals = plot_df['Month']
        y_vals = plot_df[y]
                        
        plt.scatter(x_vals, y_vals, color='blue', label='Data')
        x_numeric = x_vals.map(lambda d: d.toordinal())
        y_numeric = y_vals

        # Trend line
        z = np.polyfit(x_numeric, y_numeric, 1)
        p = np.poly1d(z)
        plt.plot(x_vals, p(x_numeric), 'r-', label='추세선')
        
        plt.xlabel('Month')
        plt.ylabel(y)
        plt.title(f'Month vs {y}')

        plt.grid(True)
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()
    else:
        print("잘못된 선택입니다.")

def show_st_sales(st_sales_page, option_var):
    selected_file = os.path.join(ROOT_DIR, '매출합계표', option_var.get())
    df, headers_dict, dropdown_list = load_sales_data(selected_file)
        
    # Title
    title_label = ttk.Label(st_sales_page, text="옵션을 선택하세요", font=("Arial", 14))
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    x_label = ttk.Label(st_sales_page, text="X축:")
    x_label.grid(row=1, column=0, sticky='e', padx=(10, 5), pady=5)
    options1 = dropdown_list

    selected_option1 = tk.StringVar(value=options1[0])
    dropdown1 = ttk.OptionMenu(st_sales_page, selected_option1, selected_option1.get(), *options1)
    dropdown1.grid(row=1, column=1, sticky='w', padx=(5, 10), pady=5)

    y_label = ttk.Label(st_sales_page, text="Y축:")
    y_label.grid(row=2, column=0, sticky='e', padx=(10, 5), pady=5)
    options2 = dropdown_list

    selected_option2 = tk.StringVar(value=options2[0])
    dropdown2 = ttk.OptionMenu(st_sales_page, selected_option2, selected_option2.get(), *options2)
    dropdown2.grid(row=2, column=1, sticky='w', padx=(5, 10), pady=5)

    st_submit_button = tk.Button(st_sales_page, text="선택 완료", command=lambda: create_st_plot(df, headers_dict, selected_option1, selected_option2), font=("Arial", 14))
    st_submit_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))


def show_lt_sales(lt_sales_page, lt_sales_listbox, sales_file_list):
    selected_files = [sales_file_list[i] for i in lt_sales_listbox.curselection()]
    headers_dict = {}

    if selected_files:
        first = selected_files[0]
        df, headers_dict, dropdown_list = load_sales_data(os.path.join(ROOT_DIR, "매출합계표",first))

    # Title
    title_label = ttk.Label(lt_sales_page, text="옵션을 선택하세요", font=("Arial", 14))
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    y_label = ttk.Label(lt_sales_page, text="Y축:")
    y_label.grid(row=2, column=0, sticky='e', padx=(10, 5), pady=5)
    options = dropdown_list

    if options:
        selected_option = tk.StringVar(value=options[0])
    else:
        selected_option = tk.StringVar(value="")  # 또는 기본값 설정
        print("⚠ options 리스트가 비어 있습니다.")
    dropdown = ttk.OptionMenu(lt_sales_page, selected_option, selected_option.get(), *options)
    dropdown.grid(row=2, column=1, sticky='w', padx=(5, 10), pady=5)

    df_by_yymm = {}
    dfs = []

    for file in selected_files:
        yymm = os.path.splitext(file)[0]  # Extract '2401' from '2401.xlsx'
        path = os.path.join(ROOT_DIR, '매출합계표', file)
        try:
            df = pd.read_excel(path)

            try:
                date = datetime.strptime(yymm, "%y%m")  # Convert '2401' to datetime
            except ValueError:
                print(f"Skipping invalid YYMM: {yymm}")
                continue

            df = df.copy()
            df = df.iloc[-1:]  # 마지막 행만 선택
            df['YYMM'] = yymm          # For string-based tracking
            df['Month'] = date         # For time-based sorting
            df_by_yymm[yymm] = df
            dfs.append(df)
        except Exception as e:
            print(f"❌ Failed to load {file}: {e}")

    # Step 2: Combine all into one DataFrame
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"✅ Combined DataFrame shape: {combined_df.shape}")
    else:
        combined_df = pd.DataFrame()
        print("⚠ No valid data files to combine.")

    lt_submit_button = tk.Button(lt_sales_page, text="선택 완료", command=lambda: create_lt_plot(combined_df, headers_dict, selected_option), font=("Arial", 14))
    lt_submit_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))