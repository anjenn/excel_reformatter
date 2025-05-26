import tkinter as tk
import os
import matplotlib.font_manager as fm
import re
from tkinter import font, ttk
from sales_fn import show_st_sales, show_lt_sales

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



######################################################################
# 프로그램 인터페이스
######################################################################

root = tk.Tk()
custom_font = font.Font(family="Malgun Gothic", size=12)
root.geometry("300x200")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.title("Excel Data Manipulation")

def show_frame(frame):
    frame.tkraise()

container = tk.Frame(root)
container.pack(fill='both', expand=True)

# --- Define pages (as frames)
main_page = tk.Frame(container)
st_sales_page = tk.Frame(container)
lt_sales_page = tk.Frame(container)

for frame in (main_page, st_sales_page, lt_sales_page):
    frame.grid(row=0, column=0, sticky='nsew')

######################################################################
# 메인 화면
######################################################################

# 1. 월별 매출
sales_file_list = get_file_list(ROOT_DIR)

input_file = os.path.join(ROOT_DIR, "매출합계표")  # 더미 엑셀 파일 
sales_file_list = [f for f in os.listdir(input_file) if os.path.isfile(os.path.join(input_file, f))]

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

lt_sales_listbox.grid(row=2, column=0, sticky='w', padx=(10, 5), pady=5)

button_lt_sales = ttk.Button(main_page, text="장기 매출", command=lambda: (show_lt_sales(lt_sales_page, lt_sales_listbox, sales_file_list), show_frame(lt_sales_page)), style='TButton')
button_lt_sales.grid(row=2, column=1, sticky='e', padx=(10, 20), pady=20)


show_frame(main_page)
root.mainloop()

# 전월, 당월, 금일매출 비교
# 연간 트렌드 분석
# 거래처별 성장률 분석 - 당월매출 / 전월매출 (성장/감소율 파악)





# 미수금 누적 거래처 분석 (누적 미수금 상위 거래처 Top 10)
# 전월대비 판매율이 낮거나 매출이 낮은 거래처 파악
# 매출 대비 실제 회수된 금액 = 입금액 / 매출액
# 거래처별 당월매출 vs 미수잔액 바차트
# 월별 매출 합계 트렌드 라인