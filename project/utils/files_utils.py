# utils/file_utils.py
import os
from typing import List
from config.settings import Config

class FileUtils:
    @staticmethod
    def get_excel_files(directory: str) -> List[str]:
        """Get list of Excel files in directory"""
        pass
    
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