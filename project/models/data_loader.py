import pandas as pd
import numpy as np
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from config.settings import Config

class DataLoader:
    def __init__(self):
        self._cache = {}
        
    def get_monthly_sales_data(self, file_path: str) -> Tuple[Optional[pd.DataFrame], Dict, List]:
        """Load sales data from Excel file with caching"""
        try:
            # Check cache first
            if file_path in self._cache:
                return self._cache[file_path]
            
            df = pd.read_excel(file_path, engine='openpyxl')
            headers_dict = Config.SALES_HEADERS
            dropdown_list = list(headers_dict.keys())
            
            # Cache the result
            result = (df, headers_dict, dropdown_list)
            self._cache[file_path] = result
            
            return result
            
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None, {}, []
        except Exception as e:
            print(f"Error loading sales data: {str(e)}")
            return None, {}, []
    
    def get_credit_sales_data(self, file_path: str) -> Tuple[Optional[pd.DataFrame], List]:
        """Load credit sales data from Excel file"""
        try:
            # Check cache first
            cache_key = f"credit_{file_path}"
            if cache_key in self._cache:
                return self._cache[cache_key]
            
            df = pd.read_excel(file_path, header=None, engine='openpyxl')
            df = df.iloc[5:]  # Skip first 5 rows
            
            # Set column names
            df.columns = [Config.CREDIT_HEADERS.get(i, f'Unnamed: {i}') 
                         for i in range(df.shape[1])]
            
            dropdown_list = list(Config.CREDIT_HEADERS.keys())
            
            # Cache the result
            result = (df, dropdown_list)
            self._cache[cache_key] = result
            
            return result
            
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None, []
        except Exception as e:
            print(f"Error loading credit data: {str(e)}")
            return None, []
    
    def get_longterm_sales_data(self, file_paths: List[str]) -> pd.DataFrame:
        print("Loading long-term sales data...")
        """Load and combine multiple sales files for long-term analysis"""
        dfs = []
        
        for file_path in file_paths:
            try:
                # Extract YYMM from filename
                filename = os.path.basename(file_path)
                yymm = os.path.splitext(filename)[0]
                
                # Load data
                df = pd.read_excel(file_path, engine='openpyxl')
                
                # Convert YYMM to date
                try:
                    date = datetime.strptime(yymm, "%y%m")
                except ValueError:
                    print(f"Invalid date format in filename: {filename}")
                    continue
                
                # Take only the last row (summary row)
                df = df.iloc[-1:].copy()
                df['YYMM'] = yymm
                df['Month'] = date
                
                dfs.append(df)
                
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
                continue
        
        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            return combined_df.sort_values(by='Month')
        
        return pd.DataFrame()
    
    def clean_data(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Clean and validate data"""
        if df is None or df.empty:
            return df
            
        cleaned_df = df.copy()
        
        # Remove last row if it contains totals
        if len(cleaned_df) > 1:
            cleaned_df = cleaned_df.iloc[:-1]
        
        # Clean numeric columns
        for col in columns:
            if col in cleaned_df.columns:
                cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
        
        # Clean product column if exists
        if Config.PRODUCT_COLUMN in cleaned_df.columns:
            cleaned_df[Config.PRODUCT_COLUMN] = (
                cleaned_df[Config.PRODUCT_COLUMN]
                .astype(str)
                .str.strip()
                .str.replace(r'\s+', ' ', regex=True)
                .replace(['', 'nan', 'NaN', 'None'], np.nan)
            )
        
        return cleaned_df
    
    def clear_cache(self):
        """Clear the data cache"""
        self._cache.clear()
    
    def get_cache_info(self) -> Dict:
        """Get information about cached data"""
        return {
            'cached_files': len(self._cache),
            'cache_keys': list(self._cache.keys())
        }