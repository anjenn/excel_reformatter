# views/lt_anal_page.py
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from tkinter import ttk
from config.settings import Config
from utils.file_utils import FileUtils
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

class LtAnalPage:
    def __init__(self, parent, controller):
    # def __init__(self, parent, controller, data):
        self.parent = parent
        self.controller = controller
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='both', expand=True)
        
        # Title
        title = ttk.Label(self.frame, text="장기 매출 트렌드 분석", 
                         font=(Config.FONT_FAMILY, Config.FONT_SIZE_TITLE, 'bold'))
        title.pack(pady=10)

        self.setup_filelist_widget()
    
    def setup_filelist_widget(self):
        """Set up monthly sales analysis section"""
        # File selection frame
        file_frame = ttk.LabelFrame(self.frame, text="파일 선택 (다중 선택 가능)")
        file_frame.pack(fill='both', expand=True, padx=20, pady=10)
        # Expand true for listbox only (needed for both filefame and listbox_frame)

        # File selection
        listbox_frame = ttk.Frame(file_frame)
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.lt_listbox = tk.Listbox(listbox_frame, selectmode='extended', height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.lt_listbox.yview)
        self.lt_listbox.config(yscrollcommand=scrollbar.set)

        self.sales_file_list = FileUtils.get_valid_file_list(FileUtils.get_file_list(Config.SALES_DIR))

        # Populate listbox
        for file in self.sales_file_list:
            self.lt_listbox.insert(tk.END, file)
        
        self.lt_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Button frame
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.lt_analyze_btn = ttk.Button(btn_frame, text="트렌드 분석", 
                                         command=lambda:self.setup_options_widget(),
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

        # Info
        info = ttk.Label(btn_frame, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", 
                        font=('Malgun Gothic', 8))
        info.pack(side='left', padx=5)

        # # Plot area # Consider having it here (not done this way in st_anal_page.py)
        # self.lt_plot_frame = ttk.Frame(longterm_frame)
        # self.lt_plot_frame.pack(fill='both', padx=20, pady=10)
        
    def setup_options_widget(self):
        # Clear previous frames if they exist
        if hasattr(self, 'option_frame'):
            self.option_frame.destroy()
        if hasattr(self, 'longterm_plot_frame'):
            self.longterm_plot_frame.destroy()

        # Option selection frame
        self.option_frame = ttk.LabelFrame(self.frame, text="옵션 선택")
        self.option_frame.pack(fill='x', padx=20, pady=10)

        # Option selection
        option_select_frame = ttk.Frame(self.option_frame)
        option_select_frame.pack(fill='x', padx=10, pady=10)
        
        self.selected_files = [self.sales_file_list[i] for i in self.lt_listbox.curselection()]

        if self.selected_files:
            first = self.selected_files[0]
            df, self.dropdown_list = FileUtils.load_sales_data(os.path.join(Config.SALES_DIR, first))

        options = self.dropdown_list
        self.selected_option = tk.StringVar(value=options[0])
        ttk.Label(option_select_frame, text=f'선택된 파일 목록: {', '.join([os.path.splitext(f)[0] for f in self.selected_files])}').pack(side='bottom', anchor='w', padx=5, pady=5)
        
        ttk.Label(option_select_frame, text="분석 항목:").pack(side='left', padx=5)
        lt_combo = ttk.Combobox(option_select_frame, textvariable=self.selected_option,
                               values=options, state='readonly')
        lt_combo.pack(side='left', padx=5)
        
        ttk.Button(option_select_frame, text="그래프 보기", 
                  command=self.setup_longterm_trend_plot).pack(side='left', padx=10)
    
    def setup_longterm_trend_plot(self):
        # Clear previous plot frame if it exists
        if hasattr(self, 'longterm_plot_frame'):
            self.longterm_plot_frame.destroy()
        if hasattr(self, 'longterm_plot_canvas'):
            self.longterm_plot_canvas.get_tk_widget().destroy()
            plt.close(self.longterm_plot_figure)

        self.longterm_plot_frame = ttk.Frame(self.frame)
        self.longterm_plot_frame.pack(fill='both', padx=20, pady=10)

        df_by_yymm = {}
        dfs = []

        for file_name in self.selected_files:
            yymm = os.path.splitext(file_name)[0]  # Extract '2401' from '2401.xlsx'
            path = os.path.join(Config.SALES_DIR, file_name)
            try:
                df = pd.read_excel(path)

                try:
                    date = datetime.strptime(yymm, "%y%m")  # Convert '2401' to datetime
                except ValueError:
                    print(f"Skipping invalid YYMM: {yymm}")
                    continue

                df = df.copy()
                df = df.iloc[-1:]  # 마지막 행만 선택
                df['YYMM'] = yymm          # For string-based tracking
                df['Month'] = date         # For time-based sorting
                df_by_yymm[yymm] = df
                dfs.append(df)
            except Exception as e:
                print(f"❌ Failed to load {file_name}: {e}")

        # Step 2: Combine all into one DataFrame
        if dfs:
            self.combined_df = pd.concat(dfs, ignore_index=True)
        else:
            self.combined_df = pd.DataFrame()

        self.create_lt_plot()

    def create_lt_plot(self):
        x_label = 'Month' # X-axis: date (from combined_df)
        y_label = self.selected_option.get() # Y-axis: selected column from dropdown

        plot_df = self.combined_df[[x_label, y_label]].copy()
        plot_df[y_label] = pd.to_numeric(plot_df[y_label], errors='coerce')
        plot_df = plot_df.dropna(subset=[x_label, y_label])

        if y_label in Config.SALES_HEADERS and not plot_df.empty:
            plot_df = plot_df.sort_values(by=x_label)

            x_data = plot_df[x_label]
            y_data = plot_df[y_label]

            # Create plot
            self.longterm_plot_figure, ax = plt.subplots(figsize=(8, 5)) # TO-DO confirm (8,5)?
            ax.plot(x_data, y_data, marker='o', linewidth=2, markersize=8, color='#2E86C1')
            ax.fill_between(x_data, y_data, alpha=0.3, color='#2E86C1')
            
            x_numeric = x_data.map(lambda d: d.toordinal())
            y_numeric = y_data

            # Add trend line
            z = np.polyfit(x_numeric, y_numeric, 1)
            p = np.poly1d(z)
            ax.plot(x_data, p(x_numeric), "r--", alpha=0.8, label='추세선')

            ax.set_xlabel('월')
            ax.set_ylabel(y_label)
            ax.set_title(f'{y_label} 장기 트렌드 분석')
            ax.grid(True, alpha=0.3)
            ax.legend()

            plt.xticks(rotation=45) # TO-DO confirm rotation
            plt.tight_layout() # TO-DO confirm tight_layout

            # Embed plot
            self.longterm_plot_canvas = FigureCanvasTkAgg(self.longterm_plot_figure, master=self.longterm_plot_frame)
            self.longterm_plot_canvas.draw()
            self.longterm_plot_canvas.get_tk_widget().pack(fill='both', expand=True)
            # Bind double-click to show popup
            self.longterm_plot_canvas.get_tk_widget().bind("<Double-Button-1>", lambda e: plt.show())
        else:
            print("잘못된 선택입니다. 유효한 데이터를 선택해주세요.")

    # Event handlers
    def on_lt_selection_change(self, event):
        """Handle long-term listbox selection change"""
        if self.lt_listbox.curselection():
            self.lt_analyze_btn.config(state='normal')
        else:
            self.lt_analyze_btn.config(state='disabled')

    def select_all_lt_files(self):
        """Select all files in long-term listbox"""
        self.lt_listbox.select_set(0, tk.END)
        self.lt_analyze_btn.config(state='normal')

    def clear_lt_selection(self):
        """Clear long-term selection"""
        self.lt_listbox.selection_clear(0, tk.END)
        self.lt_analyze_btn.config(state='disabled')