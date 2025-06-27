# views/credit_page.py
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from tkinter import ttk
from config.settings import Config
from utils.file_utils import FileUtils
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

class CreditPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='both', expand=True)
        
        # Title
        title = ttk.Label(self.frame, text="외상 매출 분석", 
                         font=(Config.FONT_FAMILY, Config.FONT_SIZE_TITLE, 'bold'))
        title.pack(pady=10)

        self.setup_filelist_widget()
    
    def setup_filelist_widget(self):
        """Set up credit sales analysis section"""
        # File selection frame
        file_frame = ttk.LabelFrame(self.frame, text="파일 선택 (다중 선택 가능)")
        file_frame.pack(fill='both', expand=True, padx=20, pady=10)
        # Expand true for listbox only (needed for both filefame and listbox_frame)

        # File selection
        listbox_frame = ttk.Frame(file_frame)
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.cs_listbox = tk.Listbox(listbox_frame, selectmode='extended', height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.cs_listbox.yview)
        self.cs_listbox.config(yscrollcommand=scrollbar.set)

        self.credit_file_list = FileUtils.get_valid_file_list(FileUtils.get_file_list(Config.CRED_SALES_DIR))

        # Populate listbox
        for file in self.credit_file_list:
            self.cs_listbox.insert(tk.END, file)
        
        self.cs_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Button frame
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.cs_analyze_btn = ttk.Button(btn_frame, text="외상 매출 분석", 
                                         command=lambda:self.setup_dashboard_widget(),
                                         state='disabled')
        self.cs_analyze_btn.pack(side='right', padx=5)
        
        select_all_btn = ttk.Button(btn_frame, text="전체 선택", 
                                  command=self.select_all_cs_files)
        select_all_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="선택 해제", 
                             command=self.clear_cs_selection)
        clear_btn.pack(side='left', padx=5)

        # Bind selection event
        self.cs_listbox.bind('<<ListboxSelect>>', self.on_cs_selection_change)

        # Info
        info = ttk.Label(btn_frame, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", 
                        font=('Malgun Gothic', 8))
        info.pack(side='left', padx=5)

        # # Plot area # Consider having it here (not done this way in st_anal_page.py)
        # self.cs_plot_frame = ttk.Frame(credit_frame)
        # self.cs_plot_frame.pack(fill='both', padx=20, pady=10)
        
    def setup_dashboard_widget(self):
        # Clear previous frames if they exist
        if hasattr(self, 'filter_frame'):
            self.filter_frame.destroy()
        if hasattr(self, 'credit_notebook'):
            self.credit_notebook.destroy()

        # Filter options
        self.filter_frame = ttk.LabelFrame(self.frame, text="필터 옵션")
        self.filter_frame.pack(fill='x', padx=20, pady=10)

        # Option selection
        filter_select_frame = ttk.Frame(self.filter_frame)
        filter_select_frame.pack(fill='x', padx=10, pady=10)
        
        self.selected_files = [self.credit_file_list[i] for i in self.cs_listbox.curselection()]
        ttk.Label(filter_select_frame, text=f'선택된 파일 목록: {', '.join([os.path.splitext(f)[0] for f in self.selected_files])}').pack(side='bottom', anchor='w', padx=5, pady=5)
        
        # Client filter
        ttk.Label(filter_select_frame, text="거래처:").pack(side='left', padx=5)
        self.client_var = tk.StringVar(value="전체")
        client_combo = ttk.Combobox(filter_select_frame, textvariable=self.client_var,
                                   values=["전체", "거래처A", "거래처B", "거래처C"], state='readonly')
        client_combo.pack(side='left', padx=5)
        
        # Period filter
        ttk.Label(filter_select_frame, text="기간:").pack(side='left', padx=5)
        self.period_var = tk.StringVar(value="당월")
        period_combo = ttk.Combobox(filter_select_frame, textvariable=self.period_var,
                                   values=["당월", "전월", "최근 3개월"], state='readonly')
        period_combo.pack(side='left', padx=5)

        # High debt filter
        self.high_debt_var = tk.BooleanVar()
        ttk.Checkbutton(filter_select_frame, text="미수잔액 100만원 이상만", 
                       variable=self.high_debt_var).pack(side='left', padx=10)
        
        ttk.Button(filter_select_frame, text="그래프 보기", 
                  command=self.setup_credit_trend_plot).pack(side='left', padx=10)  
    
        # Create tabs for different analyses
        self.credit_notebook = ttk.Notebook(self.frame)
        self.credit_notebook.pack(fill='both', padx=20, pady=10)
        
        # Tab 1: Sales vs Debt
        tab1 = ttk.Frame(self.credit_notebook)
        self.credit_notebook.add(tab1, text="매출 vs 미수잔액")
        
        # Tab 2: Debt Rate
        tab2 = ttk.Frame(self.credit_notebook)
        self.credit_notebook.add(tab2, text="미수율")
        
        # Tab 3: Monthly Comparison
        tab3 = ttk.Frame(self.credit_notebook)
        self.credit_notebook.add(tab3, text="전월 vs 당월")
        
        # Store tab references
        self.credit_tabs = {'tab1': tab1, 'tab2': tab2, 'tab3': tab3}
        
        # Create initial plots
        # self.update_credit_plots()

    def setup_credit_trend_plot(self): #To-be-modified
        # Clear previous plot frame if it exists
        if hasattr(self, 'credit_plot_frame'):
            self.credit_plot_frame.destroy()
        if hasattr(self, 'credit_plot_canvas'):
            self.credit_plot_canvas.get_tk_widget().destroy()
            plt.close(self.credit_plot_figure)

        self.credit_plot_frame = ttk.Frame(self.frame)
        self.credit_plot_frame.pack(fill='both', padx=20, pady=10)

        df_by_yymm = {}
        dfs = []

        for file_name in self.selected_files:
            yymm = os.path.splitext(file_name)[0]  # Extract '2401' from '2401.xlsx'
            path = os.path.join(Config.CRED_SALES_DIR, file_name)
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
                print(f"❌ Failed to load {file_name}: {e}")

        # Step 2: Combine all into one DataFrame
        if dfs:
            self.combined_df = pd.concat(dfs, ignore_index=True)
        else:
            self.combined_df = pd.DataFrame()

        self.create_cs_plot()

    def create_cs_plot(self):
        x_label = 'Month' # X-axis: date (from combined_df)
        y_label = self.selected_option.get() # Y-axis: selected column from dropdown

        plot_df = self.combined_df[[x_label, y_label]].copy()
        plot_df[y_label] = pd.to_numeric(plot_df[y_label], errors='coerce')
        plot_df = plot_df.dropna(subset=[x_label, y_label])

        if y_label in Config.SALES_HEADERS and not plot_df.empty:
            plot_df = plot_df.sort_values(by=x_label)

            x_data = plot_df[x_label]
            y_data = plot_df[y_label]

            # Create plot
            self.credit_plot_figure, ax = plt.subplots(figsize=(8, 5)) # TO-DO confirm (8,5)?
            ax.plot(x_data, y_data, marker='o', linewidth=2, markersize=8, color='#2E86C1')
            ax.fill_between(x_data, y_data, alpha=0.3, color='#2E86C1')
            
            x_numeric = x_data.map(lambda d: d.toordinal())
            y_numeric = y_data

            # Add trend line
            z = np.polyfit(x_numeric, y_numeric, 1)
            p = np.poly1d(z)
            ax.plot(x_data, p(x_numeric), "r--", alpha=0.8, label='추세선')

            ax.set_xlabel('월')
            ax.set_ylabel(y_label)
            ax.set_title(f'{y_label} 장기 트렌드 분석')
            ax.grid(True, alpha=0.3)
            ax.legend()

            plt.xticks(rotation=45) # TO-DO confirm rotation
            plt.tight_layout() # TO-DO confirm tight_layout

            # Embed plot
            self.credit_plot_canvas = FigureCanvasTkAgg(self.credit_plot_figure, master=self.credit_plot_frame)
            self.credit_plot_canvas.draw()
            self.credit_plot_canvas.get_tk_widget().pack(fill='both', expand=True)
            # Bind double-click to show popup
            self.credit_plot_canvas.get_tk_widget().bind("<Double-Button-1>", lambda e: plt.show())
        else:
            print("잘못된 선택입니다. 유효한 데이터를 선택해주세요.")

    # Event handlers
    def on_cs_selection_change(self, event):
        """Handle long-term listbox selection change"""
        if self.cs_listbox.curselection():
            self.cs_analyze_btn.config(state='normal')
        else:
            self.cs_analyze_btn.config(state='disabled')

    def select_all_cs_files(self):
        """Select all files in long-term listbox"""
        self.cs_listbox.select_set(0, tk.END)
        self.cs_analyze_btn.config(state='normal')

    def clear_cs_selection(self):
        """Clear long-term selection"""
        self.cs_listbox.selection_clear(0, tk.END)
        self.cs_analyze_btn.config(state='disabled')


