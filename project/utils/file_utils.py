# utils/file_utils.py
import os
import re
import pandas as pd
from typing import List
from config.settings import Config

class FileUtils:
    @staticmethod
    def get_file_list(directory):
        """Get list of Excel files in directory"""
        try:
            return [f for f in os.listdir(directory) 
                   if os.path.isfile(os.path.join(directory, f)) and f.endswith('.xlsx')]
        except FileNotFoundError:
            print(f"Directory not found: {directory}")
            return []
        
    @staticmethod
    def load_sales_data(input_file):
        directory = os.path.join(Config.SALES_DIR, input_file)
        try:
            df = pd.read_excel(directory, engine='openpyxl')  # 엑셀 파일 읽기
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {directory}")
            exit()
        dropdown_list = list(Config.SALES_HEADERS.keys())
        return df, dropdown_list

    @staticmethod
    def get_valid_file_list(file_list: List[str]) -> List[str]:
        pattern = re.compile(r'^\d{4}\.xlsx$')  # e.g., '2401.xlsx', '2512.xlsx'
        valid_files = [f for f in file_list if pattern.match(f)]
        sorted_files = sorted(valid_files, key=lambda f: int(f[:4]))  # f[:4] gets '2401'

        # TO-DO 'YYMM.xlsx 형식으로 파일명 저장 해주세요' 에러 메시지 프린트

        # get file lists

        return sorted_files
    
    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """Validate if file path exists and is readable"""
        pass
    
    @staticmethod
    def extract_date_from_filename(filename: str) -> str:
        """Extract YYMM date from filename"""
        pass
    
    @staticmethod
    def ensure_output_directory():
        """Ensure output directory exists"""
        pass