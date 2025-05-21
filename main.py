import tkinter as tk
import pandas as pd
import os
from tkinter import StringVar
from openpyxl import load_workbook, Workbook
import matplotlib.pyplot as plt


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

# 프로그램 인터페이스
df, headers_dict, dropdown_list = load_excel_data(input_file)

root = tk.Tk()
root.geometry("300x200")
root.title("Excel Data Manipulation")
# 드롭다운 메뉴 생성

selected_option1 = StringVar(root)
options1 = dropdown_list
selected_option1.set(options1[0])  # 기본값 설정

selected_option2 = StringVar(root)
options2 = dropdown_list
selected_option2.set(options2[0])  # 기본값 설정

dropdown1 = tk.OptionMenu(root, selected_option1, *options1)
dropdown1.pack(pady=20)

dropdown2 = tk.OptionMenu(root, selected_option2, *options2)
dropdown2.pack(pady=20)


def convert_to_datetime(df, col):
    if not pd.api.types.is_datetime64_any_dtype(df[col]):
        df[col] = pd.to_datetime(df[col])
    return df

def show_selected(df):
    selected_value1 = selected_option1.get()
    selected_value2 = selected_option2.get()

    col = '일자'
    if not pd.api.types.is_datetime64_any_dtype(df[col]):
        df[col] = pd.to_datetime(df[col])
    # label1.config(text=f"선택한 값: {selected_value1}")
    # label2.config(text=f"선택한 값: {selected_value2}")
    print(df.columns)

    plt.scatter(df[selected_value1].dropna(), df[selected_value2].dropna())

    # Add labels and title
    plt.xlabel('Height')
    plt.ylabel('Weight')
    plt.title('Height vs Weight')

    # create_plot(df)

def create_plot(df):
    selected_value1 = selected_option1.get()
    selected_value2 = selected_option2.get()

    # 선택된 값에 따라 데이터 처리
    if selected_value1 in headers_dict and selected_value2 in headers_dict:
        idx1 = headers_dict[selected_value1]
        idx2 = headers_dict[selected_value2]

        # 데이터 처리 로직 추가
        print(f"선택된 인덱스: {idx1}, {idx2}")
        print(df)
        df = df.iloc[:, [idx1, idx2]]

        # # 결과를 엑셀 파일로 저장
        # output_file = os.path.join(output_folder, OUTPUT_FILENAME)
        # with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        #     df.to_excel(writer, index=False)

        # print(f"결과가 {output_file}에 저장되었습니다.")
    else:
        print("잘못된 선택입니다.")

label1 = tk.Label(root, text="버튼을 눌러보세요.")
label1.pack()

label2 = tk.Label(root, text="버튼을 눌러보세요.")
label2.pack()

button = tk.Button(root, text="눌러주세요", command=show_selected(df))
button.pack()

root.mainloop()
