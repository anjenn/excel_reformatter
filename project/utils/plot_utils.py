# utils/plot_utils.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotUtils:
    # Credit analysis plots
    @staticmethod
    def plot_sales_vs_debt(data, selected_period):
        fig, ax = plt.subplots(figsize=(6, 4))
        index = range(len(data))
        bar_width = 0.35

        y1 = data['당월매출'] if selected_period.get() == "당월" else data['전월매출']
        label1 = selected_period.get() + "매출"

        ax.bar(index, y1, bar_width, label=label1, color='skyblue')
        ax.bar([i + bar_width for i in index], data['금일미수잔액'], bar_width, label='미수잔액', color='salmon')

        ax.set_xlabel('거래처명')
        ax.set_ylabel('금액 (원)')
        ax.set_title(f'{label1} vs 미수잔액')
        ax.set_xticks([i + bar_width/2 for i in index])
        ax.set_xticklabels(data['거래처명'])
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        return fig
    
    def plot_misu_rate(data):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(data['거래처명'], data['미수율'], color='orange')
        ax.set_title('미수율 (%)')
        ax.set_ylabel('미수율 (%)')
        ax.grid(axis='y')
        plt.tight_layout()
        return fig

    def plot_monthly_sales(data):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(data['거래처명'], data['전월매출'], marker='o', label='전월매출')
        ax.plot(data['거래처명'], data['당월매출'], marker='o', label='당월매출')
        ax.set_title('전월 vs 당월 매출')
        ax.set_ylabel('매출액 (원)')
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        return fig

    @staticmethod
    def setup_korean_font():
        """Set up Korean font for matplotlib"""
        pass
    
    @staticmethod
    def embed_plot_in_tkinter(parent_frame, figure):
        """Embed matplotlib figure in tkinter frame"""
        pass