# utils/file_utils.py
import os
from typing import List
from config.settings import Config
import re

class FileUtils:
    @staticmethod
    def get_file_list(directory):
        try:
            return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.xlsx')]
        except FileNotFoundError:
            return []

    @staticmethod
    def get_excel_files(directory: str) -> List[str]:
        sales_file_list = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        pattern = re.compile(r'^\d{4}\.xlsx$')  # e.g., '2401.xlsx', '2512.xlsx'
        valid_files = [f for f in sales_file_list if pattern.match(f)]
        sorted_files = sorted(valid_files, key=lambda f: int(f[:4]))  # f[:4] gets '2401'

        # TO-DO 'YYMM.xlsx 형식으로 파일명 저장 해주세요' 에러 메시지 프린트

        # get file lists

        return sorted_files
    
    # @staticmethod
    # def get_longterm_files(directory: str) -> List[str]:
    #     """Get list of long-term trend files"""
    #     lt_file_list = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    #     pattern = re.compile(r'^\d{4}\.xlsx$')
    #     valid_files = [f for f in lt_file_list if pattern.match(f)]
    #     sorted_files = sorted(valid_files, key=lambda f: int(f[:4]))  # f[:4] gets '2401'
    #     return sorted_files
    
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