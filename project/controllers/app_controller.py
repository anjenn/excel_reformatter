# controllers/app_controller.py
import tkinter as tk
from tkinter import ttk
from config.settings import Config
from models.data_loader import DataLoader
from models.sales_analyzer import SalesAnalyzer, CreditAnalyzer
from views.main_page import MainPage

class SalesAnalysisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_models()
        self.configure_window()

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.setup_ui()
    
    def setup_models(self):
        """Initialize data models"""
        self.data_loader = DataLoader()
        self.sales_analyzer = SalesAnalyzer(self.data_loader)
        self.credit_analyzer = CreditAnalyzer(self.data_loader)
    
    def setup_ui(self):
        """Set up the user interface"""
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initialize main page
        self.main_page = MainPage(main_container, self)
    
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