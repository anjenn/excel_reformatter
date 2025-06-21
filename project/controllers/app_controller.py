# controllers/app_controller.py
import tkinter as tk
from tkinter import ttk
from config.settings import Config
from models.data_loader import DataLoader
from models.sales_analyzer import SalesAnalyzer, CreditAnalyzer
from views.main_page import MainPage
from views.sales_page import SalesPage
from views.credit_page import CreditPage

class SalesAnalysisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_models()
        self.setup_ui()
        self.configure_window()
    
    def setup_models(self):
        """Initialize data models"""
        self.data_loader = DataLoader()
        self.sales_analyzer = SalesAnalyzer(self.data_loader)
        self.credit_analyzer = CreditAnalyzer(self.data_loader)
    
    def setup_ui(self):
        """Set up the user interface"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create pages
        self.main_page = MainPage(self.notebook, self)
        self.sales_page = SalesPage(self.notebook, self)
        self.credit_page = CreditPage(self.notebook, self)
        
        # Add to notebook
        self.notebook.add(self.main_page.frame, text="메인")
        self.notebook.add(self.sales_page.frame, text="매출분석")
        self.notebook.add(self.credit_page.frame, text="외상분석")
    
    def configure_window(self):
        """Configure main window"""
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
    
    def get_data_loader(self):
        """Get data loader instance"""
        return self.data_loader
    
    def get_sales_analyzer(self):
        """Get sales analyzer instance"""
        return self.sales_analyzer
    
    def get_credit_analyzer(self):
        """Get credit analyzer instance"""
        return self.credit_analyzer
    
    def run(self):
        """Run the application"""
        Config.ensure_directories()
        self.root.mainloop()