import requests
import tkinter as tk
from tkinter import Text, Scrollbar, Entry

with open('api.txt', 'r') as file:
    api = file.readline()

def get_meal(sc ,msc ,date):
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    headers = { "Content-type": "application/json" }

    payload_today = {
        "KEY": api,
        "Type": "json",
        "pIndex": 1,
        "pSize": 1,
        "ATPT_OFCDC_SC_CODE": msc,
        "SD_SCHUL_CODE": sc,
        "MLSV_YMD": date,
    }

    response_today = requests.get(url, params=payload_today, headers=headers)
    data_today = response_today.json()

    try:
        meal_data_today = data_today["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]
        cleaned_info_today = "\n".join(''.join(c for c in line if c not in '()0123456789.').strip() for line in meal_data_today.split("<br/>"))
    except KeyError:
        cleaned_info_today = "급식 정보를 불러올 수 없습니다. 이는 오늘 급식이 없거나 서버의 문제일수도 있습니다."

    return cleaned_info_today

def on_school_code_enter(event):
    middle_school_code_entry.focus()

def on_middle_school_code_enter(event):
    date_entry.focus()

def on_date_enter(event):
    show_meal_info()

def show_meal_info():
    selected_date = date_entry.get()
    meal_info = get_meal(school_code_entry.get(), middle_school_code_entry.get(), selected_date)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, meal_info)

root = tk.Tk()
root.title("급식 정보")

school_code_label = tk.Label(root, text="학교 코드:")
school_code_label.pack()

school_code_entry = tk.Entry(root)
school_code_entry.pack()
school_code_entry.bind("<Return>", on_school_code_enter)  # Bind Enter key to move to the next entry

middle_school_code_label = tk.Label(root, text="시도교육청 코드:")
middle_school_code_label.pack()

middle_school_code_entry = tk.Entry(root)
middle_school_code_entry.pack()
middle_school_code_entry.bind("<Return>", on_middle_school_code_enter)  # Bind Enter key to move to the next entry

date_label = tk.Label(root, text="날짜 (YYYYMMDD):")
date_label.pack()

date_entry = Entry(root)
date_entry.pack()
date_entry.bind("<Return>", on_date_enter)  # Bind Enter key to show_meal_info

show_meal_button = tk.Button(root, text="급식 보기", command=show_meal_info)
show_meal_button.pack()

result_text = Text(root, wrap=tk.WORD, width=40, height=10)
result_text.pack()

scrollbar = Scrollbar(root, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
