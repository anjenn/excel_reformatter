import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

class SalesAnalysisDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📊 Sales Analysis Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Sample data for demonstration
        self.sample_sales_files = ["2401.xlsx", "2402.xlsx", "2403.xlsx", "2404.xlsx", "2405.xlsx"]
        self.sample_credit_files = ["2401.xlsx", "2402.xlsx", "2403.xlsx"]
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the main user interface"""
        # Main title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=20, fill='x')
        
        title_label = ttk.Label(title_frame, text="📊 Sales Analysis Dashboard", 
                               font=('Malgun Gothic', 16, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="매출 분석 대시보드", 
                                  font=('Malgun Gothic', 10))
        subtitle_label.pack()
        
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        self.create_monthly_sales_tab()
        self.create_longterm_trend_tab()
        self.create_credit_analysis_tab()
        
    def create_monthly_sales_tab(self):
        """Create monthly sales analysis tab"""
        monthly_frame = ttk.Frame(self.notebook)
        self.notebook.add(monthly_frame, text="월별 매출 분석")
        
        # Title
        title = ttk.Label(monthly_frame, text="월별 매출 분석", 
                         font=('Malgun Gothic', 14, 'bold'))
        title.pack(pady=10)
        
        # File selection frame
        file_frame = ttk.LabelFrame(monthly_frame, text="파일 선택")
        file_frame.pack(fill='x', padx=20, pady=10)
        
        # File selection
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(file_select_frame, text="매출 파일:").pack(side='left', padx=5)
        
        self.monthly_file_var = tk.StringVar(value=self.sample_sales_files[0])
        file_combo = ttk.Combobox(file_select_frame, textvariable=self.monthly_file_var,
                                 values=self.sample_sales_files, state='readonly', width=15)
        file_combo.pack(side='left', padx=5)
        
        analyze_btn = ttk.Button(file_select_frame, text="분석 시작", 
                               command=self.show_monthly_analysis)
        analyze_btn.pack(side='right', padx=5)
        
        # Info
        info_label = ttk.Label(file_frame, text="Excel 파일을 선택하고 '분석 시작'을 클릭하세요.",
                              font=('Malgun Gothic', 8))
        info_label.pack(pady=5)
        
        # Analysis options frame (initially hidden)
        self.monthly_options_frame = ttk.LabelFrame(monthly_frame, text="분석 옵션")
        self.monthly_options_frame.pack(fill='x', padx=20, pady=10)
        self.monthly_options_frame.pack_forget()  # Hide initially
        
        # Plot area
        self.monthly_plot_frame = ttk.Frame(monthly_frame)
        self.monthly_plot_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
    def create_longterm_trend_tab(self):
        """Create long-term trend analysis tab"""
        longterm_frame = ttk.Frame(self.notebook)
        self.notebook.add(longterm_frame, text="장기 트렌드 분석")
        
        # Title
        title = ttk.Label(longterm_frame, text="장기 트렌드 분석", 
                         font=('Malgun Gothic', 14, 'bold'))
        title.pack(pady=10)
        
        # File selection frame
        file_frame = ttk.LabelFrame(longterm_frame, text="파일 선택 (다중 선택 가능)")
        file_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(file_frame)
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.lt_listbox = tk.Listbox(listbox_frame, selectmode='extended', height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.lt_listbox.yview)
        self.lt_listbox.config(yscrollcommand=scrollbar.set)
        
        # Populate listbox
        for file in self.sample_sales_files:
            self.lt_listbox.insert(tk.END, file)
        
        self.lt_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Button frame
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.lt_analyze_btn = ttk.Button(btn_frame, text="장기 트렌드 분석", 
                                       command=self.show_longterm_analysis,
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
        info = ttk.Label(btn_frame, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", 
                        font=('Malgun Gothic', 8))
        info.pack(side='left', padx=5)
        
        # Plot area
        self.lt_plot_frame = ttk.Frame(longterm_frame)
        self.lt_plot_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
    def create_credit_analysis_tab(self):
        """Create credit sales analysis tab"""
        credit_frame = ttk.Frame(self.notebook)
        self.notebook.add(credit_frame, text="외상 매출 분석")
        
        # Title
        title = ttk.Label(credit_frame, text="외상 매출 분석", 
                         font=('Malgun Gothic', 14, 'bold'))
        title.pack(pady=10)
        
        # File selection frame
        file_frame = ttk.LabelFrame(credit_frame, text="파일 선택 (다중 선택 가능)")
        file_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(file_frame)
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.credit_listbox = tk.Listbox(listbox_frame, selectmode='extended', height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.credit_listbox.yview)
        self.credit_listbox.config(yscrollcommand=scrollbar.set)
        
        # Populate listbox
        for file in self.sample_credit_files:
            self.credit_listbox.insert(tk.END, file)
        
        self.credit_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Button frame
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        self.credit_analyze_btn = ttk.Button(btn_frame, text="외상 매출 분석", 
                                           command=self.show_credit_analysis,
                                           state='disabled')
        self.credit_analyze_btn.pack(side='right', padx=5)
        
        # Bind selection event
        self.credit_listbox.bind('<<ListboxSelect>>', self.on_credit_selection_change)
        
        # Info label
        info = ttk.Label(btn_frame, text="YYMM.xlsx 형식으로 파일명 저장 해주세요", 
                        font=('Malgun Gothic', 8))
        info.pack(side='left', padx=5)
        
        # Plot area
        self.credit_plot_frame = ttk.Frame(credit_frame)
        self.credit_plot_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
    def show_monthly_analysis(self):
        """Show monthly sales analysis options and plot"""
        # Show options frame
        self.monthly_options_frame.pack(fill='x', padx=20, pady=10)
        
        # Clear previous options
        for widget in self.monthly_options_frame.winfo_children():
            widget.destroy()
        
        # Create analysis options
        options_frame = ttk.Frame(self.monthly_options_frame)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        # X-axis selection
        ttk.Label(options_frame, text="X축:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.x_var = tk.StringVar(value="상품명")
        x_combo = ttk.Combobox(options_frame, textvariable=self.x_var,
                              values=["상품명", "중량", "원가", "매가"], state='readonly')
        x_combo.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        # Y-axis selection
        ttk.Label(options_frame, text="Y축:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.y_var = tk.StringVar(value="매가총금액")
        y_combo = ttk.Combobox(options_frame, textvariable=self.y_var,
                              values=["매가총금액", "매익액", "매익율", "중량"], state='readonly')
        y_combo.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(options_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="상관관계 분석", 
                  command=self.plot_correlation).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="품목별 매출", 
                  command=self.plot_product_sales).pack(side='left', padx=5)
        
        # Create initial plot
        self.plot_correlation()
        
    def show_longterm_analysis(self):
        """Show long-term trend analysis"""
        selected_files = [self.sample_sales_files[i] for i in self.lt_listbox.curselection()]
        if not selected_files:
            messagebox.showwarning("경고", "파일을 선택해주세요.")
            return
        
        # Create options frame
        options_frame = ttk.LabelFrame(self.lt_plot_frame, text="분석 옵션")
        options_frame.pack(fill='x', pady=10)
        
        # Clear previous options
        for widget in options_frame.winfo_children():
            widget.destroy()
        
        opt_frame = ttk.Frame(options_frame)
        opt_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(opt_frame, text="분석 항목:").pack(side='left', padx=5)
        self.lt_var = tk.StringVar(value="매가총금액")
        lt_combo = ttk.Combobox(opt_frame, textvariable=self.lt_var,
                               values=["매가총금액", "매익액", "중량", "원가총금액"], state='readonly')
        lt_combo.pack(side='left', padx=5)
        
        ttk.Button(opt_frame, text="트렌드 분석", 
                  command=self.plot_longterm_trend).pack(side='left', padx=10)
        
        # Create initial plot
        self.plot_longterm_trend()
        
    def show_credit_analysis(self):
        """Show credit sales analysis"""
        selected_files = [self.sample_credit_files[i] for i in self.credit_listbox.curselection()]
        if not selected_files:
            messagebox.showwarning("경고", "파일을 선택해주세요.")
            return
        
        # Create credit analysis interface
        self.create_credit_dashboard()
        
    def create_credit_dashboard(self):
        """Create credit analysis dashboard"""
        # Clear previous content
        for widget in self.credit_plot_frame.winfo_children():
            widget.destroy()
        
        # Filter options
        filter_frame = ttk.LabelFrame(self.credit_plot_frame, text="필터 옵션")
        filter_frame.pack(fill='x', pady=10)
        
        opt_frame = ttk.Frame(filter_frame)
        opt_frame.pack(fill='x', padx=10, pady=10)
        
        # Client filter
        ttk.Label(opt_frame, text="거래처:").pack(side='left', padx=5)
        self.client_var = tk.StringVar(value="전체")
        client_combo = ttk.Combobox(opt_frame, textvariable=self.client_var,
                                   values=["전체", "거래처A", "거래처B", "거래처C"], state='readonly')
        client_combo.pack(side='left', padx=5)
        
        # Period filter
        ttk.Label(opt_frame, text="기간:").pack(side='left', padx=5)
        self.period_var = tk.StringVar(value="당월")
        period_combo = ttk.Combobox(opt_frame, textvariable=self.period_var,
                                   values=["당월", "전월", "최근 3개월"], state='readonly')
        period_combo.pack(side='left', padx=5)
        
        # High debt filter
        self.high_debt_var = tk.BooleanVar()
        ttk.Checkbutton(opt_frame, text="미수잔액 100만원 이상만", 
                       variable=self.high_debt_var).pack(side='left', padx=10)
        
        # Update button
        ttk.Button(opt_frame, text="그래프 보기", 
                  command=self.update_credit_plots).pack(side='left', padx=10)
        
        # Create tabs for different analyses
        self.credit_notebook = ttk.Notebook(self.credit_plot_frame)
        self.credit_notebook.pack(fill='both', expand=True, pady=10)
        
        # Tab 1: Sales vs Debt
        tab1 = ttk.Frame(self.credit_notebook)
        self.credit_notebook.add(tab1, text="매출 vs 미수잔액")
        
        # Tab 2: Debt Rate
        tab2 = ttk.Frame(self.credit_notebook)
        self.credit_notebook.add(tab2, text="미수율")
        
        # Tab 3: Monthly Comparison
        tab3 = ttk.Frame(self.credit_notebook)
        self.credit_notebook.add(tab3, text="전월 vs 당월")
        
        # Store tab references
        self.credit_tabs = {'tab1': tab1, 'tab2': tab2, 'tab3': tab3}
        
        # Create initial plots
        self.update_credit_plots()
        
    def plot_correlation(self):
        """Plot correlation analysis"""
        # Clear previous plot
        for widget in self.monthly_plot_frame.winfo_children():
            widget.destroy()
        
        # Create sample data
        np.random.seed(42)
        x_data = np.random.normal(100, 20, 50)
        y_data = 2 * x_data + np.random.normal(0, 10, 50)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(x_data, y_data, alpha=0.7, color='skyblue')
        
        # Add trend line
        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)
        ax.plot(x_data, p(x_data), "r--", alpha=0.8, label='추세선')
        
        ax.set_xlabel(f'{self.x_var.get()}')
        ax.set_ylabel(f'{self.y_var.get()}')
        ax.set_title(f'{self.x_var.get()} vs {self.y_var.get()} 상관관계')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=self.monthly_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def plot_product_sales(self):
        """Plot product sales analysis"""
        # Clear previous plot
        for widget in self.monthly_plot_frame.winfo_children():
            widget.destroy()
        
        # Create sample data
        products = ['제품A', '제품B', '제품C', '제품D', '제품E']
        sales = [150000, 120000, 180000, 90000, 210000]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(products, sales, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        
        ax.set_ylabel('매출액 (원)')
        ax.set_title('제품별 매출 현황')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:,.0f}',
                   ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=self.monthly_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def plot_longterm_trend(self):
        """Plot long-term trend analysis"""
        # Clear previous plot
        for widget in self.lt_plot_frame.winfo_children():
            widget.destroy()
        
        # Create sample data
        months = ['24년1월', '24년2월', '24년3월', '24년4월', '24년5월']
        values = [1200000, 1350000, 1180000, 1420000, 1380000]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(months, values, marker='o', linewidth=2, markersize=8, color='#2E86C1')
        ax.fill_between(months, values, alpha=0.3, color='#2E86C1')
        
        ax.set_ylabel(f'{self.lt_var.get()} (원)')
        ax.set_title(f'{self.lt_var.get()} 장기 트렌드 분석')
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(values):
            ax.text(i, v, f'{v:,.0f}', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=self.lt_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def update_credit_plots(self):
        """Update credit analysis plots"""
        # Sample data
        clients = ['거래처A', '거래처B', '거래처C', '거래처D', '거래처E']
        current_sales = [500000, 750000, 300000, 900000, 650000]
        previous_sales = [480000, 720000, 320000, 850000, 600000]
        debt = [100000, 150000, 80000, 200000, 120000]
        debt_rates = [20, 20, 27, 22, 18]
        
        # Plot 1: Sales vs Debt
        self.plot_sales_vs_debt(clients, current_sales, debt)
        
        # Plot 2: Debt Rate
        self.plot_debt_rate(clients, debt_rates)
        
        # Plot 3: Monthly Comparison
        self.plot_monthly_comparison(clients, current_sales, previous_sales)
        
    def plot_sales_vs_debt(self, clients, sales, debt):
        """Plot sales vs debt comparison"""
        # Clear previous plot
        for widget in self.credit_tabs['tab1'].winfo_children():
            widget.destroy()
        
        # Create plot
        fig, ax = plt.subplots(figsize=(8, 5))
        
        x = np.arange(len(clients))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, sales, width, label='매출액', color='skyblue')
        bars2 = ax.bar(x + width/2, debt, width, label='미수잔액', color='salmon')
        
        ax.set_xlabel('거래처명')
        ax.set_ylabel('금액 (원)')
        ax.set_title('매출 vs 미수잔액')
        ax.set_xticks(x)
        ax.set_xticklabels(clients)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=self.credit_tabs['tab1'])
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def plot_debt_rate(self, clients, rates):
        """Plot debt rate analysis"""
        # Clear previous plot
        for widget in self.credit_tabs['tab2'].winfo_children():
            widget.destroy()
        
        # Create plot
        fig, ax = plt.subplots(figsize=(8, 5))
        
        bars = ax.bar(clients, rates, color='orange')
        ax.set_ylabel('미수율 (%)')
        ax.set_title('거래처별 미수율')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=self.credit_tabs['tab2'])
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def plot_monthly_comparison(self, clients, current, previous):
        """Plot monthly sales comparison"""
        # Clear previous plot
        for widget in self.credit_tabs['tab3'].winfo_children():
            widget.destroy()
        
        # Create plot
        fig, ax = plt.subplots(figsize=(8, 5))
        
        ax.plot(clients, previous, marker='o', label='전월매출', linewidth=2, markersize=8)
        ax.plot(clients, current, marker='s', label='당월매출', linewidth=2, markersize=8)
        
        ax.set_ylabel('매출액 (원)')
        ax.set_title('전월 vs 당월 매출 비교')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=self.credit_tabs['tab3'])
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    # Event handlers
    def on_lt_selection_change(self, event):
        """Handle long-term listbox selection change"""
        if self.lt_listbox.curselection():
            self.lt_analyze_btn.config(state='normal')
        else:
            self.lt_analyze_btn.config(state='disabled')
            
    def on_credit_selection_change(self, event):
        """Handle credit listbox selection change"""
        if self.credit_listbox.curselection():
            self.credit_analyze_btn.config(state='normal')
        else:
            self.credit_analyze_btn.config(state='disabled')
            
    def select_all_lt_files(self):
        """Select all files in long-term listbox"""
        self.lt_listbox.select_set(0, tk.END)
        self.lt_analyze_btn.config(state='normal')
        
    def clear_lt_selection(self):
        """Clear long-term selection"""
        self.lt_listbox.selection_clear(0, tk.END)
        self.lt_analyze_btn.config(state='disabled')
        
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SalesAnalysisDashboard()
    app.run()