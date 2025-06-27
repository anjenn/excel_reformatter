import tkinter as tk
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from pages import show_frame, main_page

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
ROOT_DIR = r'c:\Users\anjen\Desktop\project\anjenn\excel_reformatter\project'  # 프로젝트 루트 디렉토리

headers_dict = {
    0: '거래처명',
    1: '전일잔액',
    2: '매출액',
    4: '입금내역',
    5: '금일잔액',
    6: '미수율',
    8: '전월매출',
    9: '판매율',
    10: '당월매출',
    11: '금일미수잔액'
}

def load_sales_data(input_file):
    try:
        df = pd.read_excel(input_file, header=None, engine='openpyxl')  # 엑셀 파일 읽기
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_file}")
        exit()

    dropdown_list = list(headers_dict.keys())
    df = df.iloc[5:]

    return df, dropdown_list

# 필터링 함수
def get_filtered_df(df, selected_client, only_high_debt):
    filtered = df.copy()
    if selected_client.get() != "전체":
        filtered = filtered[filtered['거래처명'] == selected_client.get()]
    if only_high_debt.get():
        filtered = filtered[filtered['금일미수잔액'] >= 1000000]
    return filtered

# 그래프 그리기
def draw_chart(df, tab, plot_func):
    for widget in tab.winfo_children():
        widget.destroy()
    # fig = plot_func(get_filtered_df())
    fig = plot_func(df)
    canvas = FigureCanvasTkAgg(fig, master=tab)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# 그래프 함수들
def plot_sales_vs_debt(data, selected_period):
    fig, ax = plt.subplots(figsize=(6, 4))
    index = range(len(data))
    bar_width = 0.35

    y1 = data['당월매출'] if selected_period.get() == "당월" else data['전월매출']
    label1 = selected_period.get() + "매출"

    ax.bar(index, y1, bar_width, label=label1, color='skyblue')
    ax.bar([i + bar_width for i in index], data['금일미수잔액'], bar_width, label='미수잔액', color='salmon')

    ax.set_xlabel('거래처명')
    ax.set_ylabel('금액 (원)')
    ax.set_title(f'{label1} vs 미수잔액')
    ax.set_xticks([i + bar_width/2 for i in index])
    ax.set_xticklabels(data['거래처명'])
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig

def plot_misu_rate(data):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(data['거래처명'], data['미수율'], color='orange')
    ax.set_title('미수율 (%)')
    ax.set_ylabel('미수율 (%)')
    ax.grid(axis='y')
    plt.tight_layout()
    return fig

def plot_monthly_sales(data):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(data['거래처명'], data['전월매출'], marker='o', label='전월매출')
    ax.plot(data['거래처명'], data['당월매출'], marker='o', label='당월매출')
    ax.set_title('전월 vs 당월 매출')
    ax.set_ylabel('매출액 (원)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig

def update_tabs(tab1, tab2, tab3, df):
    # draw_chart(df, tab1, plot_sales_vs_debt)
    draw_chart(df, tab2, plot_misu_rate)
    draw_chart(df, tab3, plot_monthly_sales)

def show_cred_sales(cred_sales_page, cs_listbox, cred_sales_file_list):
    input_file = r'c:\Users\anjen\Desktop\project\anjenn\excel_reformatter\project\외상매출\2504.xlsx'
    # input_file = './외상매출/2504.xlsx'
    headers_dict = {
        0: '거래처명',
        1: '전일잔액',
        2: '매출액',
        4: '입금내역',
        5: '금일잔액',
        6: '미수율',
        8: '전월매출',
        9: '판매율',
        10: '당월매출',
        11: '금일미수잔액'
    }

    df, dropdown_list = load_sales_data(input_file)
    df.columns = [headers_dict.get(i, f'Unnamed: {i}') for i in range(df.shape[1])]

    # 위젯들
    title = ttk.Label(cred_sales_page, text="📊 거래처 매출 분석 대시보드", font=("Arial", 14))
    title.pack(pady=10)

    filter_frame = ttk.Frame(cred_sales_page)
    filter_frame.pack(pady=5)

    # 선택 변수들
    selected_client = tk.StringVar(value="전체")
    selected_period = tk.StringVar(value="당월")
    only_high_debt = tk.BooleanVar(value=False)

    # 거래처 드롭다운
    clients = ["전체"] + df['거래처명'].tolist()
    ttk.Label(filter_frame, text="거래처:").pack(side="left", padx=2)
    ttk.OptionMenu(filter_frame, selected_client, *clients).pack(side="left", padx=5)

    # 기간 필터 드롭다운
    ttk.Label(filter_frame, text="기간:").pack(side="left", padx=2)
    ttk.OptionMenu(filter_frame, selected_period, "당월", "전월", "최근 3개월").pack(side="left", padx=5)

    # 미수잔액 100만원 이상 필터 체크박스
    ttk.Checkbutton(filter_frame, text="미수잔액 100만원 이상만", variable=only_high_debt).pack(side="left", padx=10)

    # 버튼
    ttk.Button(filter_frame, text="그래프 보기", command=lambda: update_tabs(tab1, tab2, tab3)).pack(side="left", padx=10)

    # 탭 생성
    tabs = ttk.Notebook(cred_sales_page)
    tabs.pack(fill="both", expand=True)

    tab1 = ttk.Frame(tabs)
    tab2 = ttk.Frame(tabs)
    tab3 = ttk.Frame(tabs)

    tabs.add(tab1, text="매출 vs 미수잔액")
    tabs.add(tab2, text="미수율")
    tabs.add(tab3, text="전월 vs 당월")

    # update_tabs(tab1, tab2, tab3)

    selected_files = [cred_sales_file_list[i] for i in cs_listbox.curselection()]
    if selected_files:
        input_file = os.path.join(ROOT_DIR, "외상매출", selected_files[0])
        # global df, headers_dict, dropdown_list
        df, dropdown_list = load_sales_data(input_file)
        df.columns = [headers_dict.get(i, f'Unnamed: {i}') for i in range(df.shape[1])]
        update_tabs(tab1, tab2, tab3, df)
    else:
        print("선택된 파일이 없습니다.")