# views/sales_page.py
import tkinter as tk
from tkinter import ttk
from config.settings import Config
from utils.file_utils import FileUtils
from utils.plot_utils import PlotUtils

class StAnalPage:
    def __init__(self, parent, controller):
    # def __init__(self, parent, controller, data):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='both', expand=True)

        # Initialize variables
        # self.data = data  # Assuming data is passed as a DataFrame or similar structure
        # self.headers_dict = data[1]
        # self.dropdown_list = data[2]
        
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
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(file_select_frame, text="매출 파일:").pack(side='left', padx=5)

        sales_file_list = FileUtils.get_file_list(Config.SALES_DIR) # get file list from Config.SALES_DIR
        self.file_var = tk.StringVar(value=sales_file_list[0])
        
        sales_file_combo = ttk.Combobox(file_select_frame, textvariable=self.file_var,
                                 values=sales_file_list, state='readonly', width=15)
        sales_file_combo.pack(side='left', padx=5)
        
        analyze_btn = ttk.Button(file_select_frame, text="파일 선택", 
                               command=self.setup_options_widget(self.file_var.get()))
        analyze_btn.pack(side='right', padx=5)

        # Info
        info_label = ttk.Label(file_frame, text="Excel 파일을 선택하고 '파일 선택' 버튼을 클릭하세요.",
                              font=('Malgun Gothic', 8))
        info_label.pack(pady=5)

    def setup_options_widget(self, selected_file):
        # Option selection frame
        self.option_frame = ttk.LabelFrame(self.frame, text="옵션 선택")
        self.option_frame.pack(fill='x', padx=20, pady=10)

        # Clear previous options
        for widget in self.option_frame.winfo_children():
            widget.destroy()

        # Option selection
        option_select_frame = ttk.Frame(self.option_frame)
        option_select_frame.pack(fill='x', padx=10, pady=10)

        df, dropdown_list = FileUtils.load_sales_data(selected_file)

        options1 = dropdown_list
        options2 = dropdown_list
        
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
                  command=self.plot_correlation).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="품목별 매출", 
                  command=self.plot_product_sales).pack(side='left', padx=5)
        
        # Create initial plot
        # self.plot_correlation()
    
    def setup_anal_widget(self):
        # Plot area
        self.monthly_plot_frame = ttk.Frame(monthly_frame)
        self.monthly_plot_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
#     def update_plot(self):
#         """Update the plot with current data"""
#         pass
    
#     def on_file_select(self, event, listbox, button): #on_selection_change
#         if listbox.curselection():
#             button.state(['!disabled'])  # Enable
#         else:
#             button.state(['disabled'])   # Disable again if deselected
    
#     def on_parameter_change(self):
#         """Handle parameter changes"""
#         pass