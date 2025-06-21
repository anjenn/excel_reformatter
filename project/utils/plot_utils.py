# utils/plot_utils.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from config.settings import Config

class PlotUtils:
    @staticmethod
    def create_correlation_plot(ax, x_data, y_data, trend_line, x_label, y_label):
        """Create correlation scatter plot"""
        pass
    
    @staticmethod
    def create_product_sales_plot(ax, product_data, title):
        """Create product sales bar plot"""
        pass
    
    @staticmethod
    def create_trend_plot(ax, x_data, y_data, trend_line, title):
        """Create trend line plot"""
        pass
    
    @staticmethod
    def create_credit_analysis_plot(ax, data_dict, plot_type):
        """Create credit analysis plots"""
        pass
    
    @staticmethod
    def setup_korean_font():
        """Set up Korean font for matplotlib"""
        pass
    
    @staticmethod
    def embed_plot_in_tkinter(parent_frame, figure):
        """Embed matplotlib figure in tkinter frame"""
        pass