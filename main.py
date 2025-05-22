import tkinter as tk
import pandas as pd
import os
from tkinter import StringVar, font
from openpyxl import load_workbook, Workbook
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 윈도우 기본 한글 폰트 설정 (예: 'Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


# 경로 설정
root_folder = os.getcwd()  # 현재 작업 디렉토리
input_file = os.path.join(root_folder, "csv", "매출합계표_03.xlsx")  # 더미 엑셀 파일 경로
output_folder = os.path.join(root_folder, "output")  # 아웃풋 폴더 경로
OUTPUT_FILENAME = "reformatted.xlsx"


# 아웃풋 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def load_excel_data(file_path):
    # 엑셀 파일 읽기
    try:
        df = pd.read_excel(input_file, engine='openpyxl')  # 엑셀 파일 읽기
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_file}")
        exit()

    headers_dict = {header: idx for idx, header in enumerate(df.columns)}
    print("헤더 인덱스:", headers_dict)

    dropdown_list = df.columns.tolist()
    print("드롭다운 리스트:", dropdown_list)

    return df, headers_dict, dropdown_list

def convert_to_datetime(df, headers_dict):
    col = '일자'
    if col in headers_dict:
        idx = headers_dict[col]
        # 데이터프레임의 해당 열을 datetime으로 변환
        df.iloc[:, idx] = pd.to_datetime(df.iloc[:, idx], errors='coerce')
    return df

def create_plot(df, headers_dict):

    df = convert_to_datetime(df, headers_dict)

    selected_value1 = selected_option1.get()
    selected_value2 = selected_option2.get()

    # 선택된 값에 따라 데이터 처리
    if selected_value1 in headers_dict and selected_value2 in headers_dict:

        col_idx1 = headers_dict[selected_value1]
        col_idx2 = headers_dict[selected_value2]
        
        x = df.iloc[:, col_idx1]
        y = df.iloc[:, col_idx2]

        x = pd.to_numeric(x, errors='coerce')
        y = pd.to_numeric(y, errors='coerce')

        mask = x.notna() & y.notna()
        x = x[mask]
        y = y[mask]
                        
        plt.scatter(x, y)
        plt.xlabel(df.columns[col_idx1])
        plt.ylabel(df.columns[col_idx2])
        plt.title("산점도")
        plt.show()
        # # 결과를 엑셀 파일로 저장
        # output_file = os.path.join(output_folder, OUTPUT_FILENAME)
        # with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        #     df.to_excel(writer, index=False)

        # print(f"결과가 {output_file}에 저장되었습니다.")
    else:
        print("잘못된 선택입니다.")


######################################################################
######################################################################
######################################################################

# 프로그램 인터페이스
df, headers_dict, dropdown_list = load_excel_data(input_file)

root = tk.Tk()
custom_font = font.Font(family="Malgun Gothic", size=12)
root.geometry("300x200")
root.title("Excel Data Manipulation")
# 드롭다운 메뉴 생성

selected_option1 = StringVar(root)
options1 = dropdown_list
selected_option1.set(options1[1])  # 기본값 설정

selected_option2 = StringVar(root)
options2 = dropdown_list
selected_option2.set(options2[2])  # 기본값 설정

dropdown1 = tk.OptionMenu(root, selected_option1, *options1)
dropdown1.grid(row=0, column=0, columnspan=2, pady=10)

dropdown2 = tk.OptionMenu(root, selected_option2, *options2)
dropdown2.grid(row=1, column=0, padx=10, pady=5)

label1 = tk.Label(root, text="버튼을 눌러보세요.", font=custom_font)
label1.grid(row=1, column=1, padx=10, pady=5)

button = tk.Button(root, text="눌러주세요", command=lambda: create_plot(df, headers_dict), font=custom_font)
button.grid(row=2, column=1, padx=10, pady=5)

root.mainloop()
