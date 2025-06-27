# views/st_anal_page.py
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

class StAnalPage:
    def __init__(self, parent, controller):
    # def __init__(self, parent, controller, data):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='both', expand=True)
        
        # Title
        title = ttk.Label(self.frame, text="월별 매출 분석", 
                         font=(Config.FONT_FAMILY, Config.FONT_SIZE_TITLE, 'bold'))
        title.pack(pady=10)

        self.setup_filelist_widget()
    
    def setup_filelist_widget(self):
        """Set up monthly sales analysis section"""
        # File selection frame
        file_frame = ttk.LabelFrame(self.frame, text="파일 선택")
        file_frame.pack(fill='x', padx=20, pady=10)

        # File selection
        combobox_frame = ttk.Frame(file_frame)
        combobox_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(combobox_frame, text="매출 파일:").pack(side='left', padx=5)

        sales_file_list = FileUtils.get_file_list(Config.SALES_DIR)
        file_var = tk.StringVar(value=sales_file_list[0])
        
        sales_file_combo = ttk.Combobox(combobox_frame, textvariable=file_var,
                                 values=sales_file_list, state='readonly', width=15)
        sales_file_combo.pack(side='left', padx=5)
        
        analyze_btn = ttk.Button(combobox_frame, text="파일 선택", 
                               command=lambda:self.setup_options_widget(file_var.get()))
        analyze_btn.pack(side='right', padx=5)

        # Info
        info_label = ttk.Label(file_frame, text="Excel 파일을 선택하고 '파일 선택' 버튼을 클릭하세요.",
                              font=('Malgun Gothic', 8))
        info_label.pack(pady=5)

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
        self.monthly_plot_frame.pack(fill='both',  padx=20, pady=10)

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
            # Bind double-click to show popup
            self.monthly_plot_canvas.get_tk_widget().bind("<Double-Button-1>", lambda e: plt.show())
    
    def setup_product_sales_plot(self):
        # Clear previous plot frame if it exists
        if hasattr(self, 'monthly_plot_frame'):
            self.monthly_plot_frame.destroy()
        if hasattr(self, 'monthly_plot_canvas'):
            self.monthly_plot_canvas.get_tk_widget().destroy()
            plt.close(self.monthly_plot_figure)

        self.monthly_plot_frame = ttk.Frame(self.frame)
        self.monthly_plot_frame.pack(fill='both', padx=20, pady=10)
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
            # Bind double-click to show popup
            self.monthly_plot_canvas.get_tk_widget().bind("<Double-Button-1>", lambda e: plt.show())