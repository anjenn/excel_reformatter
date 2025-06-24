import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
from config.settings import Config
# from models.data_loader import DataLoader
from utils.file_utils import FileUtils
# from utils.plot_utils import PlotUtils
from views.st_anal_page import StAnalPage
from views.lt_anal_page import LtAnalPage
from views.credit_page import CreditPage

class MainPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='both', expand=True)

        # Initialize variables
        self.selected_sales_file = tk.StringVar()
        self.selected_lt_files = []
        self.selected_credit_files = []
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the main page UI"""
        # Main title
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(pady=20)
        
        title = ttk.Label(title_frame, text="Sales Analysis Dashboard", 
                         font=(Config.FONT_FAMILY, 16, 'bold'))
        title.pack()

        subtitle_label = ttk.Label(title_frame, text="매출 분석 대시보드", 
                                  font=('Malgun Gothic', 10))
        subtitle_label.pack()
        
        # Create main notebook
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)

        # self.load_file_lists()

        self.setup_monthly_sales_section()
        self.setup_longterm_section()
        self.setup_credit_section()

    def setup_monthly_sales_section(self):
        # Monthly Sales Tab
        self.monthly_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monthly_frame, text="월별 매출 분석")
        self.st_anal_page = StAnalPage(self.monthly_frame, self.controller)

    def setup_longterm_section(self):
        # Long-term Trend Tab
        self.longterm_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.longterm_frame, text="장기 트렌드 분석")
        self.lt_anal_page = LtAnalPage(self.longterm_frame, self.controller)

    def setup_credit_section(self):
        # Credit Sales Tab
        self.credit_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.credit_frame, text="외상 매출 분석")
        self.credit_page = CreditPage(self.credit_frame, self.controller)