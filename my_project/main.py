import tkinter as tk
import requests
from datetime import datetime
import pyperclip  # 新增這行

import base64
import os
from logo import img

# 建立主視窗
window = tk.Tk()
window.title('診篩列印貼紙')
window.geometry('450x750')
window.resizable(True, True)

# 設置字體大小
font = ('Helvetica', 14)
big_font = ('Helvetica', 48)

default_text = "桃園市龍潭區"

# 姓名標籤與輸入框
tk.Label(window, text="姓名:", font=font).grid(
    row=0, column=0, padx=10, pady=0, sticky="w")
entry_name = tk.Entry(window, font=font, width=25)
entry_name.grid(row=0, column=1, padx=10, pady=10)

# 身分證標籤與輸入框
tk.Label(window, text="身分證字號:", font=font).grid(
    row=1, column=0, padx=10, pady=0, sticky="w")
entry_id = tk.Entry(window, font=font, width=25)
entry_id.grid(row=1, column=1, padx=20, pady=10)

# 生日標籤與輸入框
tk.Label(window, text="生日:", font=font).grid(
    row=2, column=0, padx=10, pady=0, sticky="w")
entry_birthday = tk.Entry(window, font=font, width=25)
entry_birthday.grid(row=2, column=1, padx=20, pady=10)

# 將西元日期轉換為民國日期


def convert_to_minguo(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        minguo_year = date_obj.year - 1911
        minguo_date_str = f"{minguo_year:02d}{date_obj.month:02d}{date_obj.day:02d}"
        return minguo_date_str
    except ValueError:
        return "日期格式錯誤"

# 從 API 獲取資料


def fetch_data():
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=5)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]

            full_name = first_item.get("full_name", "")
            entry_name.delete(0, tk.END)
            entry_name.insert(0, full_name)

            id_no = first_item.get("id_no", "")
            entry_id.delete(0, tk.END)
            entry_id.insert(0, id_no)

            birth_date = first_item.get("birth_date", "")
            minguo_birthday = convert_to_minguo(birth_date)
            entry_birthday.delete(0, tk.END)
            entry_birthday.insert(0, minguo_birthday)

            get_data(id_no)

        else:
            label_result.config(text="API 資料格式不正確")
    except requests.Timeout:
        window.after(0, lambda: label_result.config(
            text="API 連線超時，請重啟 API 程式!!"))
    except requests.RequestException as e:
        label_result.config(text=f"API 請求失敗: {e}")


def get_data(id_no):
    # try:
    # 如果 id_no 是 None 或空字串，就從 entry_id 中取得
    if not id_no:
        id_no = entry_id.get().strip()
    if not id_no:
        label_result.config(text="請先輸入或讀取身分證字號")
        return
    url = f"http://localhost:3000/person/{id_no}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    full_name = data.get("name", "")
    
    print(full_name)
    
    entry_name.delete(0, tk.END)
    entry_name.insert(0, full_name)
    
    # 在這裡根據 data 自動填入教育與地址
    # 教育：如果你是用按鈕來表示的話要處理狀態更新
    education = data.get("education", "")

    edu_var.set(education)
    select_education(education)

    phone = data.get("phone", "")

    entry_phone.delete(0, tk.END)
    entry_phone.insert(0, phone)

    address = data.get("address", "")

    # 設定地址文字框（你可能需要先定義 entry_address）
    entry_address.delete("1.0", tk.END)
    entry_address.insert("1.0", address)

    # 若教育是按鈕（例如用來表示學歷等級），需要判斷教育是什麼並觸發相對應按鈕狀態變化
    label_result.config(text="資料已自動填入")

    # except requests.RequestException as e:
    # label_result.config(text=f"資料讀取失敗: {e}")


# 新增一個按鈕來觸發 API 請求
btn_fetch = tk.Button(window, text="獲取健保卡資料",
                      command=fetch_data, font=font, bg="lightblue")
btn_fetch.grid(row=3, column=0, columnspan=7, padx=10, pady=10, sticky="ew")

# 創建一個變數來存儲選擇的值
edu_var = tk.StringVar(value="無")

# 單選按鈕區塊標籤
tk.Label(window, text="教育:", font=font).grid(
    row=4, column=0, padx=10, pady=0, sticky="w")

space = tk.Label(window, text="", fg="blue", justify="left", font=font)
space.grid(row=6, column=0, columnspan=7, padx=10, pady=10, sticky="ew")

# 創建一個函數來處理按鈕點擊事件


def select_education(value):
    edu_var.set(value)
    for key, button in edu_buttons.items():
        if key == value:
            button.config(bg="lightblue")
        else:
            button.config(bg="SystemButtonFace")


# 創建按鈕並將它們添加到列表中
edu_buttons = {}
edu_options = ["無", "小學", "國(初)中", "高中(職)", "專科、大學", "研究所以上"]
for i, option in enumerate(edu_options):
    button = tk.Button(window, text=option, font=font,
                       command=lambda opt=option: select_education(opt))
    if i < 3:
        button.place(x=70 + i*125, y=200, width=120, height=30)
    else:
        button.place(x=70 + (i-3)*125, y=240, width=120, height=30)
    edu_buttons[option] = button


# 電話標籤與輸入框
tk.Label(window, text="電話:", font=font).grid(
    row=7, column=0, padx=10, pady=0, sticky="w")
entry_phone = tk.Entry(window, font=font, width=25)
entry_phone.grid(row=7, column=1, padx=20, pady=10)

# 地址標籤與輸入框
tk.Label(window, text="地址:", font=font).grid(
    row=8, column=0, padx=10, pady=0, sticky="w")
entry_address = tk.Text(window, font=font, height=4,
                        width=25)  # 使用 Text 元件並設定高度和寬度
entry_address.grid(row=8, column=1, padx=20, pady=10)
entry_address.insert("1.0", default_text)

space = tk.Label(window, text="", fg="blue", justify="left", font=font)
space.grid(row=9, column=0, columnspan=7, padx=10, pady=10, sticky="ew")

# 插入文字的函數


address_var = tk.StringVar(value="上林里")

def insert_text():
    entry_address.insert(tk.END, address_var.get())

def select_address(value):
    address_var.set(value)
    insert_text()

address_options = ["上林里", "凌雲里", "龍潭里", "中正里", "上華里"]

for i, option in enumerate(address_options):
    button = tk.Button(window, text=option, font=font,
                       command=lambda opt=option: select_address(opt))
    button.place(x=20 + i * 85, y=430, width=80, height=50)



tk.Label(window, text="施作項目:", font=font).grid(
    row=10, column=0, padx=10, pady=0, sticky="w")

item_result = tk.Label(window, text="", fg="blue", justify="left", font=font)
item_result.grid(row=10, column=1, columnspan=10, padx=10, pady=10, sticky="e")

space = tk.Label(window, text="", fg="blue", justify="left", font=font)
space.grid(row=11, column=0, columnspan=7, padx=10, pady=10, sticky="ew")

item_buttons = []
item_options = ["健檢", "BC", "子抹", "HPV", "腸篩", "口篩", "ICP"]
item_scores = {"健檢": 5, "BC": 4, "子抹": 4, "HPV": 5, "腸篩": 7, "口篩": 3, "ICP": 1}
selected_options = set()
total_score = 0

buttons = {}


def select_item(option):
    global total_score
    if option in selected_options:
        selected_options.remove(option)
        total_score -= item_scores[option]
        item_buttons.remove(option)
        buttons[option].config(bg="SystemButtonFace")
    else:
        selected_options.add(option)
        total_score += item_scores[option]
        item_buttons.append(option)
        buttons[option].config(bg="yellow")
    item_result.config(text=total_score)


def clean_item():
    global total_score
    for option in item_buttons:
        buttons[option].config(bg="SystemButtonFace")
    total_score = 0
    item_buttons.clear()
    selected_options.clear()
    item_result.config(text=total_score)


for i, option in enumerate(item_options):
    button = tk.Button(window, text=option, font=font,
                       command=lambda opt=option: select_item(opt))
    button.place(x=20 + i*60, y=520, width=50, height=50)
    buttons[option] = button

item_key_map = {
    "健檢": "healthCheck",
    "BC": "bc",
    "子抹": "papSmear",
    "HPV": "hpv",
    "腸篩": "colonScreen",
    "口篩": "oralScreen",
    "ICP": "icp"
}

# 顯示輸入結果


def submit():
    global total_score

    name = entry_name.get().strip()
    id_number = entry_id.get().strip()
    education = edu_var.get().strip()
    birthday = entry_birthday.get().strip()
    phone = entry_phone.get().strip()
    # 從第一行第一個字元開始讀取，到最後一個字元結束，並去除換行符號
    address = entry_address.get("1.0", "end-1c").strip()

    items = {eng_key: (ch_key in selected_options)
             for ch_key, eng_key in item_key_map.items()}

    data = {
        "idNumber": id_number,
        "name": name,
        "birth": birthday,
        "education": education,
        "phone": phone,
        "address": address,
        "items": items
    }

    submit_data(data)

    # 將資料複製到剪貼簿
    result_text = f"{name} {id_number} {education}\n{birthday} {phone}\n{address}"
    pyperclip.copy(result_text)

    # 清空輸入框
    entry_name.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    entry_birthday.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_address.delete("1.0", tk.END)
    entry_address.insert("1.0", default_text)

    # 更新顯示結果
    label_result.config(text=result_text)
    final_item_result.config(text=total_score)

    total_score = 0
    clean_item()


def submit_data(data):
    try:
        response = requests.post("http://localhost:3000/person", json=data)
        if response.status_code == 200:
            label_result.config(text="資料提交成功！")
        else:
            label_result.config(text=f"提交失敗，狀態碼: {response.status_code}")
    except Exception as e:
        label_result.config(text=f"提交錯誤: {e}")


# 提交按鈕
btn_submit = tk.Button(window, text="提交", command=submit,
                       font=font, bg="lightgreen")
btn_submit.grid(row=12, column=0, columnspan=7, padx=10, pady=10, sticky="ew")

# 顯示輸出結果的標籤

label_result = tk.Label(window, text="", fg="blue",
                        justify="left", font=font, wraplength=350)
label_result.grid(row=13, column=0, columnspan=10,
                  padx=10, pady=10, sticky="w")

final_item_result = tk.Label(
    window, text="", fg="red", justify="left", font=big_font)
final_item_result.grid(row=13, column=1, columnspan=10,
                       padx=10, pady=10, sticky="e")

ico = open('unicorn.ico', 'wb+')
ico.write(base64.b64decode(img))  # 寫一個icon出來
ico.close()
window.iconbitmap('unicorn.ico')  # 將icon嵌上視窗
os.remove('unicorn.ico')  # 把剛剛用完的檔案刪掉

# 啟動 GUI 事件迴圈
window.mainloop()
