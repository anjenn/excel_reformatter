import os

class Config:
    ROOT_DIR = os.getcwd()
    SALES_DIR = os.path.join(ROOT_DIR, "매출합계표")
    CRED_SALES_DIR = os.path.join(ROOT_DIR, "외상매출")
    OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
    
    # Font settings
    FONT_FAMILY = 'Malgun Gothic'
    FONT_SIZE_TITLE = 14
    FONT_SIZE_NORMAL = 12
    FONT_SIZE_SMALL = 8

    # Window settings
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    WINDOW_TITLE = "Sales Analysis Dashboard"
    
    # Headers
    SALES_HEADERS = {
        '중량': 3,
        '재고판매중량': 4,
        '원가': 5,
        '원가총금액': 6,
        '공급가': 7,
        '재고판매합': 9,
        '재고판매공급가': 10,
        '매가': 12,
        '매가총금액': 13,
        '매가공급가': 14,
        '매익액': 20,
        '매익율(%)': 21,
    }
    
    CREDIT_HEADERS = {
        0: '거래처명',
        1: '전일잔액',
        2: '매출액',
        4: '입금내역',
        5: '금일잔액',
        6: '미수율',
        8: '전월매출',
        9: '판매율',
        10: '당월매출',
        11: '금일미수잔액'
    }
    PRODUCT_COLUMN = '상품명/규격/브랜드/원산지'

    PLOT_FIGSIZE = (10, 6)
    PLOT_DPI = 100

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        for directory in [cls.SALES_DIR, cls.CRED_SALES_DIR, cls.OUTPUT_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")