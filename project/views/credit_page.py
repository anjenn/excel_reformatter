# views/credit_page.py
import tkinter as tk
from tkinter import ttk
from models.data_loader import DataLoader
from config.settings import Config

class CreditPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self.setup_filelist_widget()
    
    def setup_filelist_widget(self):
        """Set up credit sales analysis section"""
        # Title
        title = ttk.Label(self.frame, text="외상 매출 분석", 
                        font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL, 'bold'))
        title.pack(pady=10)

#         # File selection frame
#         file_frame = ttk.LabelFrame(self.credit_frame, text="파일 선택 (다중 선택 가능)")
#         file_frame.pack(fill='both', expand=True, padx=20, pady=10)

#         # Listbox with scrollbar
#         listbox_frame = ttk.Frame(file_frame)
#         listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)

#         self.credit_listbox = tk.Listbox(listbox_frame, selectmode='extended', height=8)
#         # cs_listbox = tk.Listbox(main_page, selectmode='multiple', height=5, exportselection=False)
#         scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.credit_listbox.yview)
#         self.credit_listbox.config(yscrollcommand=scrollbar.set)

#         for option in DataLoader.get_credit_sales_data(self, Config.CRED_SALES_DIR):
#             self.credit_listbox.insert(tk.END, option)

#         self.credit_listbox.pack(side='left', fill='both', expand=True)
#         scrollbar.pack(side='right', fill='y')

#         # Button frame
#         btn_frame = ttk.Frame(file_frame)
#         btn_frame.pack(fill='x', padx=10, pady=5)

#         self.credit_analyze_btn = ttk.Button(btn_frame, text="외상 매출 분석", 
#                                         command=self.open_credit_analysis,
#                                         state='disabled')
#         self.credit_analyze_btn.pack(side='right', padx=5)

#         # select_all_btn = ttk.Button(btn_frame, text="전체 선택", 
#         #                         command=self.select_all_credit_files)
#         # select_all_btn.pack(side='left', padx=5)

#         # clear_btn = ttk.Button(btn_frame, text="선택 해제", 
#         #                     command=self.clear_credit_selection)
#         # clear_btn.pack(side='left', padx=5)

#         # Bind selection event
#         self.credit_listbox.bind('<<ListboxSelect>>', CreditPage.on_file_select)

#         # Info label
#         info = ttk.Label(btn_frame, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", font=("Arial", 8))
#         info.pack(side='left', padx=5)

#     def setup_options_widget(self):
#         input_file = './외상매출/2504.xlsx' #dummy tester file
#         folder_path = Config.CRED_SALES_FILE_LIST

# #         cred_sales_dir = os.path.join(ROOT_DIR, "외상매출")  # 더미 엑셀 파일 
# # cred_sales_file_list = [f for f in os.listdir(cred_sales_dir) if os.path.isfile(os.path.join(cred_sales_dir, f))]

#         df, dropdown_list = DataLoader.get_credit_sales_data(input_file)
#         df.columns = [headers_dict.get(i, f'Unnamed: {i}') for i in range(df.shape[1])]

#         # 위젯들
#         title = ttk.Label(self.frame, text="📊 거래처 매출 분석 대시보드", font=("Arial", 14))
#         title.pack(pady=10)

#         filter_frame = ttk.Frame(self.frame)
#         filter_frame.pack(pady=5)

#         # 선택 변수들
#         selected_client = tk.StringVar(value="전체")
#         selected_period = tk.StringVar(value="당월")
#         only_high_debt = tk.BooleanVar(value=False)

#         # 거래처 드롭다운
#         clients = ["전체"] + df['거래처명'].tolist()
#         ttk.Label(filter_frame, text="거래처:").pack(side="left", padx=2)
#         ttk.OptionMenu(filter_frame, selected_client, *clients).pack(side="left", padx=5)

#         # 기간 필터 드롭다운
#         ttk.Label(filter_frame, text="기간:").pack(side="left", padx=2)
#         ttk.OptionMenu(filter_frame, selected_period, "당월", "전월", "최근 3개월").pack(side="left", padx=5)

#         # 미수잔액 100만원 이상 필터 체크박스
#         ttk.Checkbutton(filter_frame, text="미수잔액 100만원 이상만", variable=only_high_debt).pack(side="left", padx=10)

#         # 버튼
#         ttk.Button(filter_frame, text="그래프 보기", command=lambda: self.update_analysis(tab1, tab2, tab3)).pack(side="left", padx=10)

#         # 탭 생성
#         tabs = ttk.Notebook(self.frame)
#         tabs.pack(fill="both", expand=True)

#         tab1 = ttk.Frame(tabs)
#         tab2 = ttk.Frame(tabs)
#         tab3 = ttk.Frame(tabs)

#         tabs.add(tab1, text="매출 vs 미수잔액")
#         tabs.add(tab2, text="미수율")
#         tabs.add(tab3, text="전월 vs 당월")

#         # update_tabs(tab1, tab2, tab3)

#         selected_files = [cred_sales_file_list[i] for i in cs_listbox.curselection()]
#         if selected_files:
#             input_file = os.path.join(Config.ROOT_DIR, "외상매출", selected_files[0])
#             # global df, headers_dict, dropdown_list
#             df, headers_dict, dropdown_list = DataLoader.get_credit_sales_data(input_file)
#             df.columns = [headers_dict.get(i, f'Unnamed: {i}') for i in range(df.shape[1])]
#             self.update_analysis(tab1, tab2, tab3)
#         else:
#             print("선택된 파일이 없습니다.")

    
#     def setup_anal_widget(self):



#     def on_file_select(self, event, listbox, button):
#         """Enable button if an item is selected in the listbox"""
#         if listbox.curselection():
#             button.state(['!disabled']) 

#     def setup_filters(self):
#         filtered = df.copy()
#         if selected_client.get() != "전체":
#             filtered = filtered[filtered['거래처명'] == selected_client.get()]
#         if only_high_debt.get():
#             filtered = filtered[filtered['금일미수잔액'] >= 1000000]
#         return filtered
    
#     def setup_analysis_options(self):
#         """Set up analysis option controls"""
#         pass
    
#     def setup_plot_area(self):
#         for widget in tab.winfo_children():
#             widget.destroy()
#         fig = plot_func(get_filtered_df())
#         canvas = FigureCanvasTkAgg(fig, master=tab)
#         canvas.draw()
#         canvas.get_tk_widget().pack(fill="both", expand=True)
    
#     def apply_filters(self):
#         """Apply current filters to data"""
#         pass
    
#     def update_analysis(self):
#         draw_chart(tab1, plot_sales_vs_debt)
#         draw_chart(tab2, plot_misu_rate)
#         draw_chart(tab3, plot_monthly_sales)