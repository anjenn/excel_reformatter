# views/sales_page.py
import tkinter as tk
from tkinter import ttk
from config.settings import Config
from utils.file_utils import FileUtils  # Use relative import for sibling package

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

        self.setup_listbox_widget()
    
    def setup_listbox_widget(self):
        """Set up monthly sales analysis section"""
        # Title
        title = ttk.Label(self.frame, text="월별 매출 분석", 
                         font=(Config.FONT_FAMILY, Config.FONT_SIZE_TITLE, 'bold'))
        title.pack(pady=10)

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
                               command=self.setup_options_widget)
        analyze_btn.pack(side='right', padx=5)

        # Info
        info_label = ttk.Label(file_frame, text="Excel 파일을 선택하고 '파일 선택' 버튼을 클릭하세요.",
                              font=('Malgun Gothic', 8))
        info_label.pack(pady=5)

    def setup_options_widget(self):
        # Option selection frame
        option_frame = ttk.LabelFrame(self.frame, text="옵션 선택")
        option_frame.pack(fill='x', padx=20, pady=10)

        # File selection
        file_select_frame = ttk.Frame(option_frame)
        file_select_frame.pack(fill='x', padx=10, pady=10)

        # self.monthly_options_frame = ttk.LabelFrame(self.monthly_frame, text="분석 옵션")
        # self.monthly_options_frame.pack(fill='x', padx=20, pady=10)
        # self.monthly_options_frame.pack_forget()  # Hide initially
    
        # Title
        title_label = ttk.Label(self.frame, text="옵션을 선택하세요", font=("Arial", 14))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

#         x_label = ttk.Label(self.frame, text="X축:")
#         x_label.grid(row=1, column=0, sticky='e', padx=(10, 5), pady=5)
#         options1 = self.dropdown_list
#         print(f"Dropdown options: {options1}")  # Debugging line
        
#         # selected_option1 = tk.StringVar(value=options1[0])
#         # dropdown1 = ttk.OptionMenu(self.frame, selected_option1, selected_option1.get(), *options1)
#         # dropdown1.grid(row=1, column=1, sticky='w', padx=(5, 10), pady=5)

#         # y_label = ttk.Label(self.frame, text="Y축:")
#         # y_label.grid(row=2, column=0, sticky='e', padx=(10, 5), pady=5)
#         # options2 = self.dropdown_list

#         # selected_option2 = tk.StringVar(value=options2[0])
#         # dropdown2 = ttk.OptionMenu(self.frame, selected_option2, selected_option2.get(), *options2)
#         # dropdown2.grid(row=2, column=1, sticky='w', padx=(5, 10), pady=5)

#         # st_submit_button = tk.Button(self.frame, text="Submit", command=lambda: create_st_plot(df, headers_dict, selected_option1, selected_option2), font=("Arial", 12))
#         # st_submit_button.grid(row=3, column=0, sticky='e', padx=(10, 5), pady=5)

#         # st_submit_button = tk.Button(self.frame, text="품목별", command=lambda: create_st_bar_chart(df, selected_option1), font=("Arial", 12))
#         # st_submit_button.grid(row=3, column=1, sticky='e', padx=(10, 5), pady=5)

#         # back_button = tk.Button(self.frame, text="Back", command=lambda: show_frame(main_page), font=("Arial", 12))
#         # back_button.grid(row=3, column=2, sticky='w', padx=(5, 10), pady=5)
    
    def setup_anal_widget(self):
        # Plot area
        self.monthly_plot_frame = ttk.Frame(monthly_frame)
        self.monthly_plot_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
#     def setup_controls(self):
#         """Set up analysis controls"""
#         pass

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