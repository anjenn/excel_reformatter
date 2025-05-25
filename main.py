import tkinter as tk
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import re
from tkinter import font, ttk
from datetime import datetime

# 윈도우 기본 한글 폰트 설정 (예: 'Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


# 경로 설정
ROOT_DIR = os.getcwd()  # 현재 작업 디렉토리
output_folder = os.path.join(ROOT_DIR, "output")  # 아웃풋 폴더 경로

# 아웃풋 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def get_file_list(directory):
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.xlsx')]
    except FileNotFoundError:
        return []

def load_excel_data(input_file):
    # 엑셀 파일 읽기
    try:
        df = pd.read_excel(input_file, engine='openpyxl')  # 엑셀 파일 읽기
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_file}")
        exit()

    headers_dict = {
        col: idx for idx, col in enumerate(df.columns)
        if df[col].iloc[1:].notna().any()  # 첫 행 제외한 나머지 행에 데이터가 하나라도 있으면 포함
    }
    dropdown_list = list(headers_dict.keys())

    return df, headers_dict, dropdown_list

def convert_to_datetime(df, headers_dict):
    col = '일자'
    if col in headers_dict:
        idx = headers_dict[col]
        # 데이터프레임의 해당 열을 datetime으로 변환
        df.iloc[:, idx] = pd.to_datetime(df.iloc[:, idx], errors='coerce')
    return df

def create_plot(df, headers_dict, opt1, opt2):
    plt.cla()
    df = df.iloc[:-1] # 마지막 행 제거
    df = convert_to_datetime(df, headers_dict)

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


######################################################################
# 프로그램 인터페이스
######################################################################

root = tk.Tk()
custom_font = font.Font(family="Malgun Gothic", size=12)
root.geometry("300x200")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.title("Excel Data Manipulation")

def show_total_sales(trigger_button, option_var):
    selected_file = os.path.join(ROOT_DIR, '매출합계표', option_var.get())
    df, headers_dict, dropdown_list = load_excel_data(selected_file)
    
    trigger_button.grid_remove()
    
    # Title
    title_label = ttk.Label(root, text="옵션을 선택하세요", font=("Arial", 14))
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    x_label = ttk.Label(root, text="X축:")
    x_label.grid(row=1, column=0, sticky='e', padx=(10, 5), pady=5)
    options1 = dropdown_list

    selected_option1 = tk.StringVar(value=options1[0])
    dropdown1 = ttk.OptionMenu(root, selected_option1, selected_option1.get(), *options1)
    dropdown1.grid(row=1, column=1, sticky='w', padx=(5, 10), pady=5)

    y_label = ttk.Label(root, text="Y축:")
    y_label.grid(row=2, column=0, sticky='e', padx=(10, 5), pady=5)
    options2 = dropdown_list

    selected_option2 = tk.StringVar(value=options2[0])
    dropdown2 = ttk.OptionMenu(root, selected_option2, selected_option2.get(), *options2)
    dropdown2.grid(row=2, column=1, sticky='w', padx=(5, 10), pady=5)

    submit_button = tk.Button(root, text="선택 완료", command=lambda: create_plot(df, headers_dict, selected_option1, selected_option2), font=custom_font)
    submit_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

    # 숨김 버튼 제거
    button_monthly.grid_remove()

def show_lt_sales(trigger_button, lt_sales_listbox):
    selected = [sales_file_list[i] for i in lt_sales_listbox.curselection()]
    trigger_button.grid_remove()

    # Title
    title_label = ttk.Label(root, text="옵션을 선택하세요", font=("Arial", 14))
    title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    df_by_yymm = {}

    for file in selected:
        yymm = os.path.splitext(file)[0]  # Extract '2401' from '2401.xlsx'
        path = os.path.join(ROOT_DIR, '매출합계표', file)
        try:
            df = pd.read_excel(path)
            df['YYMM'] = yymm  # Optional: add a column for tracking
            df_by_yymm[yymm] = df
        except Exception as e:
            print(f"Failed to load {file}: {e}")

    dfs = []

    for yymm, df in df_by_yymm.items():
        try:
            date = datetime.strptime(yymm, "%y%m")  # Convert '2401' to datetime
            df = df.copy()
            df['Month'] = date
            dfs.append(df)
        except ValueError:
            print(f"Skipping invalid YYMM: {yymm}")

    # Step 2: Combine all into one DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)

    # Step 3: Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(combined_df['Month'], combined_df['공급가'], color='blue')
    plt.title('Sales Volume Over Time')
    plt.xlabel('Month')
    plt.ylabel('Sales Volume')
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

######################################################################
# 메인 화면
######################################################################

# 1. 월별 매출
sales_file_list = get_file_list(ROOT_DIR)

input_file = os.path.join(ROOT_DIR, "매출합계표")  # 더미 엑셀 파일 
sales_file_list = [f for f in os.listdir(input_file) if os.path.isfile(os.path.join(input_file, f))]

file_var = tk.StringVar(value=sales_file_list[0])
file_dropdown = ttk.OptionMenu(root, file_var, file_var.get(), *sales_file_list)
file_dropdown.grid(row=1, column=0, sticky='w', padx=(20, 10), pady=20)

button_monthly = ttk.Button(root, text="월별 매출", command=lambda: (show_total_sales(button_monthly, file_var), file_dropdown.grid_remove()), style='TButton')
button_monthly.grid(row=1, column=1, sticky='e', padx=(10, 20), pady=20)

# 2. 장기 매출 트렌드
lt_sales_listbox = tk.Listbox(root, selectmode='multiple', height=5, exportselection=False)
pattern = re.compile(r'^\d{4}\.xlsx$')  # e.g., '2401.xlsx', '2512.xlsx'
valid_files = [f for f in sales_file_list if pattern.match(f)]
sorted_files = sorted(valid_files, key=lambda f: int(f[:4]))  # f[:4] gets '2401'

for option in sorted_files:
    lt_sales_listbox.insert(tk.END, option)

lt_sales_listbox.grid(row=2, column=0, sticky='w', padx=(10, 5), pady=5)

button_lt_sales = ttk.Button(root, text="장기 매출", command=lambda: (show_lt_sales(button_lt_sales, lt_sales_listbox), lt_sales_listbox.grid_remove()), style='TButton')
button_lt_sales.grid(row=2, column=1, sticky='e', padx=(10, 20), pady=20)



root.mainloop()

# 전월, 당월, 금일매출 비교
# 연간 트렌드 분석
# 거래처별 성장률 분석 - 당월매출 / 전월매출 (성장/감소율 파악)





# 미수금 누적 거래처 분석 (누적 미수금 상위 거래처 Top 10)
# 전월대비 판매율이 낮거나 매출이 낮은 거래처 파악
# 매출 대비 실제 회수된 금액 = 입금액 / 매출액
# 거래처별 당월매출 vs 미수잔액 바차트
# 월별 매출 합계 트렌드 라인