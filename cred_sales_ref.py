import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 샘플 데이터프레임
data = {
    '거래처명': ['A상사', 'B마트', 'C유통'],
    '전일잔액': [1000000, 200000, 300000],
    '매출액': [500000, 300000, 400000],
    '입금내역': [300000, 100000, 200000],
    '금일잔액': [1200000, 400000, 500000],
    '미수율': [240, 133.3, 125],
    '결재관련': ['현금', '30일 외상', '60일 외상'],
    '전월매출': [800000, 350000, 450000],
    '판매율': [0.9, 0.85, 0.95],
    '당월매출': [1200000, 300000, 420000],
    '금일미수잔액': [1200000, 400000, 500000]
}
df = pd.DataFrame(data)

# tkinter UI 설정
root = tk.Tk()
root.title("거래처 매출/미수 분석")
root.geometry("800x600")

# 거래처 선택
selected_client = tk.StringVar()
selected_client.set("전체")

def get_filtered_df():
    if selected_client.get() == "전체":
        return df
    else:
        return df[df['거래처명'] == selected_client.get()]

def draw_chart(tab, plot_func):
    for widget in tab.winfo_children():
        widget.destroy()

    fig = plot_func(get_filtered_df())
    canvas = FigureCanvasTkAgg(fig, master=tab)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# 그래프 함수들
def plot_sales_vs_debt(data):
    fig, ax = plt.subplots(figsize=(6, 4))
    index = range(len(data))
    bar_width = 0.35

    ax.bar(index, data['당월매출'], bar_width, label='당월매출', color='skyblue')
    ax.bar([i + bar_width for i in index], data['금일미수잔액'], bar_width, label='미수잔액', color='salmon')

    ax.set_xlabel('거래처명')
    ax.set_ylabel('금액 (원)')
    ax.set_title('당월매출 vs 미수잔액')
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

# 상단 제목
title = ttk.Label(root, text="📊 거래처 매출 분석 대시보드", font=("맑은 고딕", 16))
title.pack(pady=10)

# 드롭다운 + 버튼
filter_frame = ttk.Frame(root)
filter_frame.pack(pady=5)

clients = ["전체"] + df['거래처명'].tolist()
dropdown = ttk.OptionMenu(filter_frame, selected_client, *clients)
dropdown.pack(side="left", padx=5)

refresh_btn = ttk.Button(filter_frame, text="그래프 보기", command=lambda: update_tabs())
refresh_btn.pack(side="left", padx=5)

# 탭 생성
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tab3 = ttk.Frame(tabs)

tabs.add(tab1, text="당월매출 vs 미수잔액")
tabs.add(tab2, text="미수율 비교")
tabs.add(tab3, text="월별 매출 추이")

# 탭 업데이트
def update_tabs():
    draw_chart(tab1, plot_sales_vs_debt)
    draw_chart(tab2, plot_misu_rate)
    draw_chart(tab3, plot_monthly_sales)

# 초기 화면
update_tabs()

# 시작
root.mainloop()
