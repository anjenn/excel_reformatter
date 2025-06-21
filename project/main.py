import tkinter as tk
import os
import matplotlib.font_manager as fm
import re
from tkinter import font, ttk
from project.views.sales_fn import show_st_sales, show_lt_sales
from project.views.cred_sales_fn import show_cred_sales
from project.pages import root, show_frame, main_page, st_sales_page, lt_sales_page, cred_sales_page

# 경로 설정
ROOT_DIR = os.getcwd()  # 현재 작업 디렉토리
output_folder = os.path.join(ROOT_DIR, "output")  # 아웃풋 폴더 경로

# class DataManager:
#     def __init__(self):
#         self._cache = {}
        
#     def get_sales_data(self, filepath):
#         if filepath in self._cache:
#             return self._cache[filepath]
            
#         data = self._load_and_validate(filepath)
#         self._cache[filepath] = data
#         return data


# 아웃풋 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def get_file_list(directory):
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.xlsx')]
    except FileNotFoundError:
        return []

def on_lt_selection_change(event):
    if lt_sales_listbox.curselection():
        button_lt_sales.state(['!disabled'])  # Enable
    else:
        button_lt_sales.state(['disabled'])   # Disable again if deselected

def on_cs_selection_change(event):
    if cs_listbox.curselection():
        button_cs_sales.state(['!disabled'])  # Enable
    else:
        button_cs_sales.state(['disabled'])   # Disable again if deselected
######################################################################
# 메인 화면
######################################################################
custom_font = font.Font(family="Malgun Gothic", size=12)
root.geometry("350x650")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.title("Excel Data Manipulation")

# 1. 월별 매출
monthly_label = ttk.Label(main_page, text="[ 월별 매출 확인 ]", font=("Arial", 14))
monthly_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

sales_dir = os.path.join(ROOT_DIR, "매출합계표")  # 더미 엑셀 파일 
sales_file_list = [f for f in os.listdir(sales_dir) if os.path.isfile(os.path.join(sales_dir, f))]

file_var = tk.StringVar(value=sales_file_list[0])
file_dropdown = ttk.OptionMenu(main_page, file_var, file_var.get(), *sales_file_list)
file_dropdown.grid(row=1, column=0, sticky='w', padx=(20, 10), pady=20)

button_monthly = ttk.Button(main_page, text="월별 매출", command=lambda: (show_st_sales(st_sales_page, file_var), show_frame(st_sales_page)), style='TButton')
button_monthly.grid(row=1, column=1, sticky='e', padx=(10, 20), pady=20)

# 2. 장기 매출 트렌드
lt_sales_listbox = tk.Listbox(main_page, selectmode='multiple', height=5, exportselection=False)
pattern = re.compile(r'^\d{4}\.xlsx$')  # e.g., '2401.xlsx', '2512.xlsx'
valid_files = [f for f in sales_file_list if pattern.match(f)]
sorted_files = sorted(valid_files, key=lambda f: int(f[:4]))  # f[:4] gets '2401'

for option in sorted_files:
    lt_sales_listbox.insert(tk.END, option)

interval_label = ttk.Label(main_page, text="[ 장기 매출 확인 ]", font=("Arial", 14))
interval_label.grid(row=2, column=0, columnspan=2, pady=(10, 20))

interval_info = ttk.Label(main_page, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", font=("Arial", 8))
interval_info.grid(row=3, column=0, columnspan=2, pady=(10, 20))

lt_sales_listbox.grid(row=4, column=0, sticky='w', padx=(10, 5), pady=5)

button_lt_sales = ttk.Button(main_page, text="장기 매출", command=lambda: (show_lt_sales(lt_sales_page, lt_sales_listbox, sales_file_list), show_frame(lt_sales_page)), style='TButton')
button_lt_sales.grid(row=4, column=1, sticky='e', padx=(10, 20), pady=20)
button_lt_sales.state(['disabled'])  # Make the button unclickable initially

lt_sales_listbox.bind('<<ListboxSelect>>', on_lt_selection_change)

# if lt_sales_listbox.curselection().count() > 0:
#     button_lt_sales.state(['!disabled'])  # Enable the button if at least one item is selected

# 3. 외상 매출 분석
cred_sales_dir = os.path.join(ROOT_DIR, "외상매출")  # 더미 엑셀 파일 
cred_sales_file_list = [f for f in os.listdir(cred_sales_dir) if os.path.isfile(os.path.join(cred_sales_dir, f))]

cs_listbox = tk.Listbox(main_page, selectmode='multiple', height=5, exportselection=False)
pattern = re.compile(r'^\d{4}\.xlsx$')  # e.g., '2401.xlsx', '2512.xlsx'
valid_files = [f for f in cred_sales_file_list if pattern.match(f)]
sorted_files = sorted(valid_files, key=lambda f: int(f[:4]))  # f[:4] gets '2401'
for option in sorted_files:
    cs_listbox.insert(tk.END, option)
cs_label = ttk.Label(main_page, text="[ 외상 매출 분석 ]", font=("Arial", 14))
cs_label.grid(row=5, column=0, columnspan=2, pady=(10, 20))
cs_info = ttk.Label(main_page, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", font=("Arial", 8))
cs_info.grid(row=6, column=0, columnspan=2, pady=(10, 20))
cs_listbox.grid(row=7, column=0, sticky='w', padx=(10, 5), pady=5)
button_cs_sales = ttk.Button(main_page, text="외상 매출 분석", command=lambda: (show_cred_sales(cred_sales_page, cs_listbox, cred_sales_file_list), show_frame(cred_sales_page)), style='TButton')
button_cs_sales.grid(row=7, column=1, sticky='e', padx=(10, 20), pady=20)
button_cs_sales.state(['disabled'])  # Make the button unclickable initially
cs_listbox.bind('<<ListboxSelect>>', on_cs_selection_change)


show_frame(main_page)
root.mainloop()