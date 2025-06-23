import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from config.settings import Config

class SalesAnalyzer:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def analyze_correlation(self, df: pd.DataFrame, x_col: str, y_col: str, 
                          headers_dict: Dict) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Analyze correlation between two variables"""
        if not df.empty and x_col in headers_dict and y_col in headers_dict:
            col_idx1 = headers_dict[x_col]
            col_idx2 = headers_dict[y_col]
            
            # Clean data
            df_clean = self.data_loader.clean_data(df, [df.columns[col_idx1], df.columns[col_idx2]])
            
            x = pd.to_numeric(df_clean.iloc[:, col_idx1], errors='coerce')
            y = pd.to_numeric(df_clean.iloc[:, col_idx2], errors='coerce')
            
            # Remove NaN values
            mask = x.notna() & y.notna()
            x_clean = x[mask]
            y_clean = y[mask]
            
            # Calculate trend line
            if len(x_clean) > 1:
                z = np.polyfit(x_clean, y_clean, 1)
                trend_line = np.poly1d(z)
                return x_clean, y_clean, trend_line(x_clean)
            
            x_label = df.columns[col_idx1]
            y_label = df.columns[col_idx2]
            
        return np.array([]), np.array([]), np.array([])
    
    def analyze_product_sales(self, df: pd.DataFrame, value_col: str) -> pd.Series:
        """Analyze sales by product"""
        if df.empty or Config.PRODUCT_COLUMN not in df.columns:
            return pd.Series()
        
        # Clean data
        df_clean = self.data_loader.clean_data(df, [value_col])
        df_clean = df_clean.dropna(subset=[Config.PRODUCT_COLUMN, value_col])
        
        # df = df.copy()
        # df.loc[:, PRODUCT] = df[PRODUCT].astype(str).str.strip()
        # df.loc[:, PRODUCT] = df[PRODUCT].str.replace(r'\s+', ' ', regex=True)
        # df.loc[:, PRODUCT] = df[PRODUCT].replace(['', 'nan', 'NaN', 'None'], np.nan)
        # df.loc[:, selected1] = pd.to_numeric(df[selected1], errors='coerce')
        # df = df.dropna(subset=[PRODUCT, selected1])  # Remove missing values

        # Group by product and sum
        grouped = df_clean.groupby(Config.PRODUCT_COLUMN)[value_col].sum()
        return grouped.sort_values(ascending=False)
    
    def analyze_long_term_trend(self, combined_df: pd.DataFrame, 
                               value_col: str) -> Tuple[pd.Series, pd.Series, Optional[np.ndarray]]:
        """Analyze long-term trends"""
        if combined_df.empty or value_col not in combined_df.columns:
            return pd.Series(), pd.Series(), None
        
        # Sort by date and clean data
        df_sorted = combined_df.sort_values(by='Month')
        df_sorted[value_col] = pd.to_numeric(df_sorted[value_col], errors='coerce')
        df_clean = df_sorted.dropna(subset=['Month', value_col])
        
        if df_clean.empty:
            return pd.Series(), pd.Series(), None
        
        x_vals = df_clean['Month']
        y_vals = df_clean[value_col]
        
        # Calculate trend line
        trend_line = None
        if len(x_vals) > 1:
            x_numeric = x_vals.map(lambda d: d.toordinal())
            z = np.polyfit(x_numeric, y_vals, 1)
            p = np.poly1d(z)
            trend_line = p(x_numeric)
        
        return x_vals, y_vals, trend_line

class CreditAnalyzer:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def filter_data(self, df: pd.DataFrame, client_filter: str = None, 
                   min_debt: float = None) -> pd.DataFrame:
        """Filter credit data based on criteria"""
        if df is None or df.empty:
            return pd.DataFrame()
        
        filtered_df = df.copy()
        
        # Filter by client
        if client_filter and client_filter != "전체":
            filtered_df = filtered_df[filtered_df['거래처명'] == client_filter]
        
        # Filter by minimum debt
        if min_debt is not None:
            debt_col = '금일미수잔액'
            if debt_col in filtered_df.columns:
                filtered_df[debt_col] = pd.to_numeric(filtered_df[debt_col], errors='coerce')
                filtered_df = filtered_df[filtered_df[debt_col] >= min_debt]
        
        return filtered_df
    
    def get_sales_vs_debt_data(self, df: pd.DataFrame, period: str = "당월") -> Dict:
        """Get data for sales vs debt analysis"""
        if df is None or df.empty:
            return {}
        
        sales_col = '당월매출' if period == "당월" else '전월매출'
        debt_col = '금일미수잔액'
        client_col = '거래처명'
        
        # Clean numeric columns
        for col in [sales_col, debt_col]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with NaN values
        df_clean = df.dropna(subset=[client_col, sales_col, debt_col])
        
        return {
            'clients': df_clean[client_col].tolist(),
            'sales': df_clean[sales_col].tolist(),
            'debt': df_clean[debt_col].tolist(),
            'period': period
        }
    
    def get_debt_rate_data(self, df: pd.DataFrame) -> Dict:
        """Get debt rate analysis data"""
        if df is None or df.empty:
            return {}
        
        rate_col = '미수율'
        client_col = '거래처명'
        
        # Clean data
        if rate_col in df.columns:
            df[rate_col] = pd.to_numeric(df[rate_col], errors='coerce')
        
        df_clean = df.dropna(subset=[client_col, rate_col])
        
        return {
            'clients': df_clean[client_col].tolist(),
            'rates': df_clean[rate_col].tolist()
        }
    
    def get_monthly_comparison_data(self, df: pd.DataFrame) -> Dict:
        """Get monthly sales comparison data"""
        if df is None or df.empty:
            return {}
        
        current_col = '당월매출'
        previous_col = '전월매출'
        client_col = '거래처명'
        
        # Clean numeric columns
        for col in [current_col, previous_col]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df_clean = df.dropna(subset=[client_col, current_col, previous_col])
        
        return {
            'clients': df_clean[client_col].tolist(),
            'current_sales': df_clean[current_col].tolist(),
            'previous_sales': df_clean[previous_col].tolist()
        }