import tkinter as tk
import requests
from datetime import datetime
import pyperclip  # 新增這行

# 建立主視窗
window = tk.Tk()
window.title('使用者資訊輸入')
window.geometry('450x700')
window.resizable(True, True)

# 設置字體大小
font = ('Helvetica', 14)

default_text = "桃園市龍潭區"

# 姓名標籤與輸入框
tk.Label(window, text="姓名:", font=font).grid(row=0, column=0, padx=10, pady=0, sticky="w")
entry_name = tk.Entry(window, font=font, width=25)
entry_name.grid(row=0, column=1, padx=10, pady=10)

# 身分證標籤與輸入框
tk.Label(window, text="身分證字號:", font=font).grid(row=1, column=0, padx=10, pady=0, sticky="w")
entry_id = tk.Entry(window, font=font, width=25)
entry_id.grid(row=1, column=1, padx=20, pady=10)

# 生日標籤與輸入框
tk.Label(window, text="生日:", font=font).grid(row=2, column=0, padx=10, pady=0, sticky="w")
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
        response = requests.get("http://127.0.0.1:8000")
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
            
        else:
            label_result.config(text="API 資料格式不正確")
    except requests.RequestException as e:
        label_result.config(text=f"API 請求失敗: {e}")

# 新增一個按鈕來觸發 API 請求
btn_fetch = tk.Button(window, text="獲取身分證資料", command=fetch_data, font=font, bg="lightblue")
btn_fetch.grid(row=3, column=0, columnspan=7, padx=10, pady=10, sticky="ew")

# 創建一個變數來存儲選擇的值
edu_var = tk.StringVar(value="無")

# 單選按鈕區塊標籤
tk.Label(window, text="教育:", font=font).grid(row=4, column=0, padx=10, pady=0, sticky="w")

space = tk.Label(window, text="", fg="blue", justify="left", font=font)
space.grid(row=6, column=0, columnspan=7, padx=10, pady=10, sticky="ew")

# 創建一個函數來處理按鈕點擊事件
def select_education(value):
    edu_var.set(value)
    for button in edu_buttons:
        if button['text'] == value:
            button.config(bg="lightblue")
        else:
            button.config(bg="SystemButtonFace")

# 創建按鈕並將它們添加到列表中
edu_buttons = []
edu_options = ["無", "小學", "國(初)中", "高中(職)", "專科、大學", "研究所以上"]
for i, option in enumerate(edu_options):
    
    if option == "無":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_education(opt))
        button.place(x=70 + i*100, y=200, width=120, height=30)  # 設定按鈕的絕對位置和大小
        edu_buttons.append(button)
    elif option == "小學":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_education(opt))
        button.place(x=90 + i*100, y=200, width=120, height=30)  # 設定按鈕的絕對位置和大小
        edu_buttons.append(button)
    elif option == "國(初)中":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_education(opt))
        button.place(x=110 + i*100, y=200, width=120, height=30)
        edu_buttons.append(button)
    elif option == "高中(職)":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_education(opt))
        button.place(x=70 + (i-3)*100, y=240, width=120, height=30)
        edu_buttons.append(button)
    elif option == "專科、大學":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_education(opt))
        button.place(x=90 + (i-3)*100, y=240, width=120, height=30)
        edu_buttons.append(button)
    elif option == "研究所以上":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_education(opt))
        button.place(x=110 + (i-3)*100, y=240, width=120, height=30)
        edu_buttons.append(button)
        
   
# 電話標籤與輸入框
tk.Label(window, text="電話:", font=font).grid(row=7, column=0, padx=10, pady=0, sticky="w")
entry_phone = tk.Entry(window, font=font, width=25)
entry_phone.grid(row=7, column=1, padx=20, pady=10)

# 地址標籤與輸入框
tk.Label(window, text="地址:", font=font).grid(row=8, column=0, padx=10, pady=0, sticky="w")
entry_address = tk.Text(window, font=font, height=4, width=25)  # 使用 Text 元件並設定高度和寬度
entry_address.grid(row=8, column=1, padx=20, pady=10)
entry_address.insert("1.0", default_text)

# 插入文字的函數
def insert_text():
    entry_address.insert(tk.END, address_var.get())
    
space = tk.Label(window, text="", fg="blue", justify="left", font=font)
space.grid(row=9, column=0, columnspan=7, padx=10, pady=10, sticky="ew")

address_var = tk.StringVar(value="凌雲里")

def select_address(value):
    address_var.set(value)
    insert_text()

address_buttons = []
address_options = ["凌雲里", "龍祥里", "八德里", "聖德里"]

for i, option in enumerate(address_options):

    
    if option == "凌雲里":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_address(opt))
        button.place(x=20 + i*100, y=430, width=100, height=50)  # 設定按鈕的絕對位置和大小
    elif option == "龍祥里":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_address(opt))
        button.place(x=25 + i*100, y=430, width=100, height=50)
    elif option == "八德里":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_address(opt))
        button.place(x=30 + i*100, y=430, width=100, height=50)
    elif option == "聖德里":
        button = tk.Button(window, text=option, font=font, command=lambda opt=option: select_address(opt))
        button.place(x=35 + i*100, y=430, width=100, height=50)


# 顯示輸入結果
def submit():
    name = entry_name.get()
    id_number = entry_id.get()
    education = edu_var.get()
    birthday = entry_birthday.get()
    phone = entry_phone.get()
    address = entry_address.get("1.0", "end-1c")  # 從第一行第一個字元開始讀取，到最後一個字元結束，並去除換行符號
    
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

# 提交按鈕
btn_submit = tk.Button(window, text="提交", command=submit, font=font, bg="lightgreen")
btn_submit.grid(row=10, column=0, columnspan=7, padx=10, pady=10, sticky="ew")

# 顯示輸出結果的標籤
label_result = tk.Label(window, text="", fg="blue", justify="left", font=font)
label_result.grid(row=11, column=0, columnspan=10, padx=10, pady=10, sticky="ew")

# 啟動 GUI 事件迴圈
window.mainloop()
