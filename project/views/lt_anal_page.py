# views/lt_anal_page.py
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import ttk
from config.settings import Config
from utils.file_utils import FileUtils
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

class LtAnalPage:
    def __init__(self, parent, controller):
    # def __init__(self, parent, controller, data):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='both', expand=True)
        
        # Title
        title = ttk.Label(self.frame, text="장기 트렌드 분석", 
                         font=(Config.FONT_FAMILY, Config.FONT_SIZE_TITLE, 'bold'))
        title.pack(pady=10)

        self.setup_filelist_widget()
    
    def setup_filelist_widget(self):
        """Set up monthly sales analysis section"""
        # File selection frame
        file_frame = ttk.LabelFrame(self.frame, text="파일 선택 (다중 선택 가능)")
        file_frame.pack(fill='both', expand=True, padx=20, pady=10)
        # TO-DO: review expand=True, as it may not be needed

        # File selection
        listbox_frame = ttk.Frame(file_frame)
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.lt_listbox = tk.Listbox(listbox_frame, selectmode='extended', height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.lt_listbox.yview)
        self.lt_listbox.config(yscrollcommand=scrollbar.set)

        sales_file_list = FileUtils.get_file_list(Config.SALES_DIR)

        # Populate listbox
        for file in sales_file_list:
            self.lt_listbox.insert(tk.END, file)
        
        self.lt_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Button frame
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.lt_analyze_btn = ttk.Button(btn_frame, text="장기 트렌드 분석", 
                                       command=self.setup_options_widget, # TO-DO: replace the function
                                       state='disabled')
        self.lt_analyze_btn.pack(side='right', padx=5)
        
        select_all_btn = ttk.Button(btn_frame, text="전체 선택", 
                                  command=self.setup_options_widget)
        select_all_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="선택 해제", 
                             command=self.setup_options_widget)
        clear_btn.pack(side='left', padx=5)

        # Bind selection event
        # self.lt_listbox.bind('<<ListboxSelect>>', self.on_lt_selection_change)

        # Info
        info = ttk.Label(btn_frame, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", 
                        font=('Malgun Gothic', 8))
        info.pack(side='left', padx=5)

        # # Plot area # Consider having it here (not done this way in st_anal_page.py)
        # self.lt_plot_frame = ttk.Frame(longterm_frame)
        # self.lt_plot_frame.pack(fill='both', expand=True, padx=20, pady=10)




# TO-DO: update from this point
    def setup_options_widget(self, selected_file):
        # Clear previous frames if they exist
        if hasattr(self, 'option_frame'):
            self.option_frame.destroy()
        if hasattr(self, 'monthly_plot_frame'):
            self.monthly_plot_frame.destroy()

        # Option selection frame
        self.option_frame = ttk.LabelFrame(self.frame, text="옵션 선택")
        self.option_frame.pack(fill='x', padx=20, pady=10)

        # Option selection
        option_select_frame = ttk.Frame(self.option_frame)
        option_select_frame.pack(fill='x', padx=10, pady=10)

        self.df, self.dropdown_list = FileUtils.load_sales_data(selected_file)

        options1 = self.dropdown_list
        options2 = self.dropdown_list
        
        ttk.Label(option_select_frame, text="X축:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.selected_option1 = tk.StringVar(value=options1[0])
        dropdown1 = ttk.Combobox(option_select_frame, textvariable=self.selected_option1,
                                   values=options1, state='readonly')
        dropdown1.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        ttk.Label(option_select_frame, text="Y축:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.selected_option2 = tk.StringVar(value=options2[0])
        dropdown2 = ttk.Combobox(option_select_frame, textvariable=self.selected_option2,
                                   values=options2, state='readonly')
        dropdown2.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        # Buttons
        btn_frame = ttk.Frame(option_select_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="상관관계 분석",
                  command=lambda:self.setup_correlation_plot()).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="품목별 매출", 
                  command=lambda:self.setup_product_sales_plot()).pack(side='left', padx=5)
    
    def setup_correlation_plot(self):
        # Clear previous plot frame if it exists
        if hasattr(self, 'monthly_plot_frame'):
            self.monthly_plot_frame.destroy()
        if hasattr(self, 'monthly_plot_canvas'):
            self.monthly_plot_canvas.get_tk_widget().destroy()
            plt.close(self.monthly_plot_figure)

        self.monthly_plot_frame = ttk.Frame(self.frame)
        self.monthly_plot_frame.pack(fill='both', expand=True, padx=20, pady=10)

        cleaned_df = self.df.iloc[:-1] # 마지막 행 제거
        selected1 = self.selected_option1.get()
        selected2 = self.selected_option2.get()
        headers_dict = Config.SALES_HEADERS

        if selected1 in headers_dict and selected2 in headers_dict:
            col_idx1 = headers_dict[selected1]
            col_idx2 = headers_dict[selected2]

            x = pd.to_numeric(cleaned_df.iloc[:, col_idx1], errors='coerce')
            y = pd.to_numeric(cleaned_df.iloc[:, col_idx2], errors='coerce')

            x_data = x[x.notna() & y.notna()] # NaN 값 제거 mask 적용
            y_data = y[x.notna() & y.notna()]

            # Create plot
            self.monthly_plot_figure, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(x_data, y_data, alpha=0.7, color='skyblue')
            
            # Add trend line
            z = np.polyfit(x_data, y_data, 1)
            p = np.poly1d(z)
            ax.plot(x_data, p(x_data), "r--", alpha=0.8, label='추세선')
            
            ax.set_xlabel(f'{selected1}')
            ax.set_ylabel(f'{selected2}')
            ax.set_title(f'{selected1} vs {selected2} 상관관계')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Embed plot
            self.monthly_plot_canvas = FigureCanvasTkAgg(self.monthly_plot_figure, master=self.monthly_plot_frame)
            self.monthly_plot_canvas.draw()
            self.monthly_plot_canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def setup_product_sales_plot(self):
        # Clear previous plot frame if it exists
        if hasattr(self, 'monthly_plot_frame'):
            self.monthly_plot_frame.destroy()
        if hasattr(self, 'monthly_plot_canvas'):
            self.monthly_plot_canvas.get_tk_widget().destroy()
            plt.close(self.monthly_plot_figure)

        self.monthly_plot_frame = ttk.Frame(self.frame)
        self.monthly_plot_frame.pack(fill='both', expand=True, padx=20, pady=10)
        PRODUCT = Config.PRODUCT_COLUMN

        cleaned_df = self.df.iloc[:-1] # 마지막 행 제거
        selected1 = self.selected_option1.get()
        # TO-DO: add a note that only selected1 is used for product sales plot
        headers_dict = Config.SALES_HEADERS

        if selected1 in headers_dict:
            df = cleaned_df.copy()
            df.loc[:, PRODUCT] = df[PRODUCT].astype(str).str.strip()
            df.loc[:, PRODUCT] = df[PRODUCT].str.replace(r'\s+', ' ', regex=True)
            df.loc[:, PRODUCT] = df[PRODUCT].replace(['', 'nan', 'NaN', 'None'], np.nan)
            df.loc[:, selected1] = pd.to_numeric(df[selected1], errors='coerce')
            df = df.dropna(subset=[PRODUCT, selected1])  # Remove missing values

            grouped = df.groupby(PRODUCT)[selected1].sum().sort_values(ascending=False)

            # Create plot
            self.monthly_plot_figure, ax = plt.subplots(figsize=(8, 5))
            products = grouped.index.tolist()
            sales = grouped.values.tolist()

            self.monthly_plot_figure, ax = plt.subplots(figsize=(8, 5))
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']  # Extend or adjust as needed

            bars = ax.bar(products, sales, color=colors[:len(products)])

            ax.set_xlabel('제품')
            ax.set_ylabel(f'{selected1} 합계')
            ax.set_title(f'제품별 {selected1} 총합')
            ax.grid(axis='y', alpha=0.3)
            ax.tick_params(axis='x', rotation=45)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:,.0f}',
                    ha='center', va='bottom')
            
            plt.tight_layout()

            # Embed plot
            self.monthly_plot_canvas = FigureCanvasTkAgg(self.monthly_plot_figure, master=self.monthly_plot_frame)
            self.monthly_plot_canvas.draw()
            self.monthly_plot_canvas.get_tk_widget().pack(fill='both', expand=True)