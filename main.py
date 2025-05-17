import tkinter as tk
import pandas as pd
import os
from openpyxl import load_workbook, Workbook


# 경로 설정
root_folder = os.getcwd()  # 현재 작업 디렉토리
input_file = os.path.join(root_folder, "dummy.xlsx")  # 더미 엑셀 파일 경로
output_folder = os.path.join(root_folder, "output")  # 아웃풋 폴더 경로
OUTPUT_FILENAME = "reformatted.xlsx"


# 아웃풋 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 엑셀 파일 읽기
try:
    df = pd.read_excel(input_file, engine='openpyxl')  # 엑셀 파일 읽기
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {input_file}")
    exit()

# 'hello world'를 추가 (첫 번째 셀에 삽입 예시)
df.iloc[0, 0] = "hello world"  # 0, 0은 첫 번째 행과 열

# 수정된 데이터프레임을 아웃풋 폴더에 저장
output_file = os.path.join(output_folder, OUTPUT_FILENAME)
df.to_excel(output_file, index=False, engine='openpyxl')  # 인덱스를 제외하고 저장

print(f"파일이 성공적으로 저장되었습니다: {output_file}")

# 프로그램 인터페이스
def say_hello():
    label.config(text="안녕하세요!")

root = tk.Tk()
root.title("나의 첫 윈도우 프로그램")

label = tk.Label(root, text="버튼을 눌러보세요.")
label.pack()

button = tk.Button(root, text="눌러주세요", command=say_hello)
button.pack()

root.mainloop()
