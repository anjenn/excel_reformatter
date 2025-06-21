import tkinter as tk
from tkinter import ttk, messagebox
import re
from config.settings import Config

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
        self.load_file_lists()
    
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
        """Set up monthly sales analysis section"""
        # Title
        title = ttk.Label(self.monthly_frame, text="월별 매출 분석", 
                         font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL, 'bold'))
        title.pack(pady=10)
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.monthly_frame, text="파일 선택")
        file_frame.pack(fill='x', padx=20, pady=10)
        
        self.sales_file_combo = ttk.Combobox(file_frame, textvariable=self.selected_sales_file,
                                           state='readonly', width=50)
        self.sales_file_combo.pack(side='left', padx=10, pady=10)
        
        # Analysis button
        analyze_btn = ttk.Button(file_frame, text="분석 시작", 
                               command=self.open_sales_analysis)
        analyze_btn.pack(side='right', padx=10, pady=10)
        
        # Info label
        info = ttk.Label(self.monthly_frame, 
                        text="Excel 파일을 선택하고 '분석 시작'을 클릭하세요.",
                        font=(Config.FONT_FAMILY, Config.FONT_SIZE_SMALL))
        info.pack(pady=5)
    
    def setup_longterm_section(self):
        """Set up long-term trend analysis section"""
        # Title
        title = ttk.Label(self.longterm_frame, text="장기 트렌드 분석", 
                         font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL, 'bold'))
        title.pack(pady=10)
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.longterm_frame, text="파일 선택 (다중 선택 가능)")
        file_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(file_frame)
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.lt_listbox = tk.Listbox(listbox_frame, selectmode='extended', height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.lt_listbox.yview)
        self.lt_listbox.config(yscrollcommand=scrollbar.set)
        
        self.lt_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Button frame
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.lt_analyze_btn = ttk.Button(btn_frame, text="장기 트렌드 분석", 
                                       command=self.open_longterm_analysis,
                                       state='disabled')
        self.lt_analyze_btn.pack(side='right', padx=5)
        
        select_all_btn = ttk.Button(btn_frame, text="전체 선택", 
                                  command=self.select_all_lt_files)
        select_all_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="선택 해제", 
                             command=self.clear_lt_selection)
        clear_btn.pack(side='left', padx=5)
        
        # Bind selection event
        self.lt_listbox.bind('<<ListboxSelect>>', self.on_lt_selection_change)
        
        # Info label
        info =



def setup_credit_section(self):
        """Set up credit sales analysis section"""
        pass
    
def load_file_lists(self):
    """Load available files into UI components"""
    pass

def open_sales_analysis(self):
    """Open sales analysis window"""
    pass

def open_longterm_analysis(self):
    """Open long-term analysis window"""
    pass

def open_credit_analysis(self):
    """Open credit analysis window"""
    pass