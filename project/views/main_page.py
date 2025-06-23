import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
from config.settings import Config
# from models.data_loader import DataLoader
# from utils.files_utils import FileUtils
# from utils.plot_utils import PlotUtils
from views.st_anal_page import StAnalPage
from views.lt_anal_page import LtAnalPage
from views.credit_page import CreditPage

class MainPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)

        self.st_anal_page = StAnalPage(self.frame, self.controller)
        self.lt_anal_page = LtAnalPage(self.frame, self.controller)
        self.credit_page = CreditPage(self.frame, self.controller)
        
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

        self.st_anal_page = StAnalPage(self.monthly_frame, self.controller,)
        self.lt_anal_page = LtAnalPage(self.longterm_frame, self.controller)
        self.credit_page = CreditPage(self.credit_frame, self.controller)
    
    def setup_monthly_sales_section(self):
        self.st_anal_page.setup_listbox_widget()
        # StAnalPage.setup_options_widget()
        # StAnalPage.setup_anal_widget()

    def setup_longterm_section(self):
        self.lt_anal_page.setup_listbox_widget()
        # LtAnalPage.setup_options_widget()
        # LtAnalPage.setup_anal_widget()

    def setup_credit_section(self):
        self.credit_page.setup_listbox_widget()
        # CreditPage.setup_options_widget()
        # CreditPage.setup_anal_widget()
