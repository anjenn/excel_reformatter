import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
from config.settings import Config
from models.data_loader import DataLoader
from utils.files_utils import FileUtils
from utils.plot_utils import PlotUtils
from views.st_anal_page import StAnalPage
from views.lt_anal_page import LtAnalPage
from views.credit_page import CreditPage

class MainPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)
        
        # Initialize variables
        self.selected_sales_file = tk.StringVar()
        self.selected_lt_files = []
        self.selected_credit_files = []
        
        self.setup_ui()
        # self.load_file_lists()
    
    def setup_ui(self):
        """Set up the main page UI"""
        # Main title
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(pady=20)
        
        title = ttk.Label(title_frame, text="📊 Sales Analysis Dashboard", 
                         font=(Config.FONT_FAMILY, Config.FONT_SIZE_TITLE, 'bold'))
        title.pack()
        
        # Create notebook for different sections
        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Monthly Sales Tab
        self.monthly_frame = ttk.Frame(notebook)
        notebook.add(self.monthly_frame, text="월별 매출 분석")
        self.setup_monthly_sales_section()
        
        # Long-term Trend Tab
        self.longterm_frame = ttk.Frame(notebook)
        notebook.add(self.longterm_frame, text="장기 트렌드 분석")
        self.setup_longterm_section()
        
        # Credit Sales Tab
        self.credit_frame = ttk.Frame(notebook)
        notebook.add(self.credit_frame, text="외상 매출 분석")
        self.setup_credit_section()
    
    def setup_monthly_sales_section(self):
        StAnalPage.setup_query_widget()
        StAnalPage.setup_analysis_widget()
        StAnalPage.setup_plot_area()

    def setup_longterm_section(self):
        LtAnalPage.setup_query_widget()
        LtAnalPage.setup_analysis_widget()
        LtAnalPage.setup_plot_area()

    def setup_credit_section(self):
        """Set up credit sales analysis section"""
        # Title
        title = ttk.Label(self.credit_frame, text="외상 매출 분석", 
                        font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL, 'bold'))
        title.pack(pady=10)

        # File selection frame
        file_frame = ttk.LabelFrame(self.credit_frame, text="파일 선택 (다중 선택 가능)")
        file_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Listbox with scrollbar
        listbox_frame = ttk.Frame(file_frame)
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.credit_listbox = tk.Listbox(listbox_frame, selectmode='extended', height=8)
        # cs_listbox = tk.Listbox(main_page, selectmode='multiple', height=5, exportselection=False)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.credit_listbox.yview)
        self.credit_listbox.config(yscrollcommand=scrollbar.set)

        for option in DataLoader.get_credit_sales_data(self, Config.CRED_SALES_DIR):
            self.credit_listbox.insert(tk.END, option)

        self.credit_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Button frame
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)

        self.credit_analyze_btn = ttk.Button(btn_frame, text="외상 매출 분석", 
                                        command=self.open_credit_analysis,
                                        state='disabled')
        self.credit_analyze_btn.pack(side='right', padx=5)

        # select_all_btn = ttk.Button(btn_frame, text="전체 선택", 
        #                         command=self.select_all_credit_files)
        # select_all_btn.pack(side='left', padx=5)

        # clear_btn = ttk.Button(btn_frame, text="선택 해제", 
        #                     command=self.clear_credit_selection)
        # clear_btn.pack(side='left', padx=5)

        # Bind selection event
        self.credit_listbox.bind('<<ListboxSelect>>', CreditPage.on_file_select)

        # Info label
        info = ttk.Label(btn_frame, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", font=("Arial", 8))
        info.pack(side='left', padx=5)