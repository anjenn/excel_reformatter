# views/sales_page.py
import tkinter as tk
from tkinter import ttk
from config.settings import Config

class LtAnalPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self.setup_filelist_widget()

    def setup_filelist_widget(self):
        """Set up long-term trend analysis section"""
        # Title
        title = ttk.Label(self.frame, text="장기 트렌드 분석", 
                         font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL, 'bold'))
        title.pack(pady=10)
        
    #     # File selection frame
    #     file_frame = ttk.LabelFrame(self.longterm_frame, text="파일 선택 (다중 선택 가능)")
    #     file_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
    #     # Listbox with scrollbar
    #     listbox_frame = ttk.Frame(file_frame)
    #     listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
    #     self.lt_listbox = tk.Listbox(listbox_frame, selectmode='extended', height=8)
    #     scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.lt_listbox.yview)
    #     self.lt_listbox.config(yscrollcommand=scrollbar.set)
        
    #     for option in FileUtils.get_file_list(Config.SALES_DIR):
    #         self.lt_listbox.insert(tk.END, option)

    #     self.lt_listbox.pack(side='left', fill='both', expand=True)
    #     scrollbar.pack(side='right', fill='y')
        
    #     # Button frame
    #     btn_frame = ttk.Frame(file_frame)
    #     btn_frame.pack(fill='x', padx=10, pady=5)
        
    #     self.lt_analyze_btn = ttk.Button(btn_frame, text="장기 트렌드 분석", 
    #                                    command=self.open_longterm_analysis,
    #                                    state='disabled')
    #     self.lt_analyze_btn.pack(side='right', padx=5)
        
    #     select_all_btn = ttk.Button(btn_frame, text="전체 선택", 
    #                               command=DataLoader.get_longterm_sales_data)
    #     select_all_btn.pack(side='left', padx=5)
        
    #     clear_btn = ttk.Button(btn_frame, text="선택 해제",
    #                          command=self.clear_lt_selection)
    #     clear_btn.pack(side='left', padx=5)
        
    #     # Bind selection event
    #     self.lt_listbox.bind('<<ListboxSelect>>', LtAnalPage.on_selection_change)
        
    #     # Info label
    #     info = ttk.Label(btn_frame, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", font=("Arial", 8))
    #     info.pack(side='left', padx=5)
    
    # def setup_options_widget(self, lt_sales_listbox):
    #     selected_files = [sales_file_list[i] for i in lt_sales_listbox.curselection()]
    #     headers_dict = {}

    #     if selected_files:
    #         first = selected_files[0]
    #         df, headers_dict, dropdown_list = load_sales_data(os.path.join(ROOT_DIR, "매출합계표",first))

    #     # Title
    #     title_label = ttk.Label(self.frame, text="옵션을 선택하세요", font=("Arial", 14))
    #     title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    #     y_label = ttk.Label(self.frame, text="Y축:")
    #     y_label.grid(row=2, column=0, sticky='e', padx=(10, 5), pady=5)
    #     options = dropdown_list

    #     if options:
    #         selected_option = tk.StringVar(value=options[0])
    #     else:
    #         selected_option = tk.StringVar(value="")  # 또는 기본값 설정
    #         print("⚠ options 리스트가 비어 있습니다.")
    #     dropdown = ttk.OptionMenu(self.frame, selected_option, selected_option.get(), *options)
    #     dropdown.grid(row=2, column=1, sticky='w', padx=(5, 10), pady=5)

    #     df_by_yymm = {}
    #     dfs = []

    #     for file in selected_files:
    #         yymm = os.path.splitext(file)[0]  # Extract '2401' from '2401.xlsx'
    #         path = os.path.join(ROOT_DIR, '매출합계표', file)
    #         try:
    #             df = pd.read_excel(path)

    #             try:
    #                 date = datetime.strptime(yymm, "%y%m")  # Convert '2401' to datetime
    #             except ValueError:
    #                 print(f"Skipping invalid YYMM: {yymm}")
    #                 continue

    #             df = df.copy()
    #             df = df.iloc[-1:]  # 마지막 행만 선택
    #             df['YYMM'] = yymm          # For string-based tracking
    #             df['Month'] = date         # For time-based sorting
    #             df_by_yymm[yymm] = df
    #             dfs.append(df)
    #         except Exception as e:
    #             print(f"❌ Failed to load {file}: {e}")

    #     # Step 2: Combine all into one DataFrame
    #     if dfs:
    #         combined_df = pd.concat(dfs, ignore_index=True)
    #     else:
    #         combined_df = pd.DataFrame()

    #     lt_submit_button = tk.Button(self.frame, text="Submit", command=lambda: create_lt_plot(combined_df, headers_dict, selected_option), font=("Arial", 12))
    #     lt_submit_button.grid(row=3, column=0, sticky='e', padx=(10, 5), pady=5)

    #     back_button2 = tk.Button(self.frame, text="Back", command=lambda: show_frame(main_page), font=("Arial", 12))
    #     back_button2.grid(row=3, column=1, sticky='w', padx=(5, 10), pady=5)
    
    # def setup_anal_widget()

    # def setup_controls(self):
    #     """Set up analysis controls"""
    #     pass
    
    # def setup_plot_area(self):
    #     """Set up plotting area"""
    #     pass
    
    # def update_plot(self):
    #     """Update the plot with current data"""
    #     pass
    
    # def on_selection_change(self, event, listbox, button): #on_selection_change
    #     if listbox.curselection():
    #         button.state(['!disabled'])  # Enable
    #     else:
    #         button.state(['disabled'])   # Disable again if deselected

    # def clear_lt_selection(self):
    #     """Clear long-term selection"""
    #     self.lt_listbox.selection_clear(0, tk.END)
    #     self.lt_analyze_btn.config(state='disabled')