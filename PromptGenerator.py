import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import pyperclip
import rag as rag
import configparser
import os

# 環境ファイル読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
# ルートパス
root_path = config_ini['DEFAULT']['ROOT_PATH']
# URLリスト
urllist_path = config_ini['DEFAULT']['URLLIST_FILE_PATH']
# ロードデータパス
load_data_path=config_ini['DEFAULT']['LOAD_DATA_PATH']
# モデル保存パス
model_name=config_ini['DEFAULT']['MODEL_NAME']

# フォルダ・ファイル作成
if not os.path.exists(root_path):
    os.makedirs(root_path)
if not os.path.exists(load_data_path):
    os.makedirs(load_data_path)
if not os.path.isfile(urllist_path):
    with open(urllist_path,"w"):
        pass

# ツール起動時DB読み込み
init_result = rag.read_db(model_name)

# プロンプト生成
def generate_prompt():
    input_text = entry.get()
    if input_text == "":
        msg = "質問を入力してください。"
    else:
        msg = rag.create_prompt(input_text)
    
    prompt_label.config(text=f"プロンプト文({input_text}) :")
    count_label.config(text=f"(文字数：{len(msg)}) ")
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, msg)

# クリップボードにコピー
def copy_to_clipboard():
    text_to_copy = result_text.get(1.0, tk.END)
    pyperclip.copy(text_to_copy)
    tkinter.messagebox.showinfo("クリップボードにコピー", "プロンプト文がクリップボードにコピーされました。GAIに貼り付けて実行してください。")

# 画面クリア
def clear_result():
    entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)
    message_text.delete(1.0, tk.END)
    prompt_label.config(text="プロンプト文:")
    count_label.config(text="")

# データベース更新
def update_database():
    res = rag.update_database(load_data_path, model_name)
    if res is not None:
        message_text.insert(0.0, res + "\n")
    tkinter.messagebox.showinfo("DB更新", "データベースが更新されました。")

# WEBページ取得
def get_webpage():
    res = rag.get_webpage(load_data_path, urllist_path)
    if res is not None:
        message_text.insert(0.0, res + "\n")
    tkinter.messagebox.showinfo("WEBページ取得", "WEBページ取得が完了しました。")

# アプリケーション終了
def exit_application():
    root.destroy()

# メインウィンドウの作成
root = tk.Tk()
root.title("Prompt Generator for GAI")

# ウィンドウサイズを設定
window_width = 500  # 少し小さく変更
window_height = 420
x_position = (root.winfo_screenwidth() - window_width) // 2
y_position = (root.winfo_screenheight() - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# タブの作成
tab_control = ttk.Notebook(root)

# タブ1
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='プロンプト生成')

tool_label = tk.Label(tab1, text="プロンプト生成ツール")
tool_label.pack()

entry_frame1 = tk.Frame(tab1)
entry_frame1.pack(pady=10)

question_label = tk.Label(entry_frame1, text="質問文:")
question_label.pack(anchor=tk.W)

entry = tk.Entry(entry_frame1, width=30)
entry.pack(side=tk.LEFT)

generate_button = tk.Button(entry_frame1, text="プロンプト生成", command=generate_prompt)
generate_button.pack(side=tk.LEFT, padx=10)

entry_frame2 = tk.Frame(tab1)
entry_frame2.pack(pady=10)

prompt_label = tk.Label(entry_frame2, text="プロンプト文:")
prompt_label.pack(anchor=tk.W)

result_text = tk.Text(entry_frame2, height=10, width=60)
result_text.pack()

count_label = tk.Label(entry_frame2, text="")
count_label.pack(anchor=tk.W,side=tk.LEFT)

copy_button = tk.Button(entry_frame2, text="クリップボードにコピー", command=copy_to_clipboard)
copy_button.pack(pady=2, side=tk.RIGHT)

button_frame = tk.Frame(tab1)
button_frame.pack(pady=10)

clear_button = tk.Button(button_frame, text="クリア", command=clear_result)
clear_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(button_frame, text="終了", command=exit_application)
exit_button.pack(side=tk.LEFT, padx=5)

# タブ2
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='設定')

urllist_frame = tk.Frame(tab2)
urllist_frame.pack(pady=10)
url_label = tk.Label(urllist_frame, text="以下のURLリストからWEBページを取得します。：")
url_label.pack(anchor=tk.W)
url_text = tk.Text(urllist_frame, height=1,width=60)
url_text.pack()
url_text.insert(tk.END, urllist_path)
webpage_button = tk.Button(urllist_frame, text="取得", command=get_webpage)
webpage_button.pack(side=tk.RIGHT, padx=5)

folder_frame = tk.Frame(tab2)
folder_frame.pack(pady=10)
loadfile_label = tk.Label(folder_frame, text="以下のファイルを読み込み込んでDBを更新します。:")
loadfile_label.pack(anchor=tk.W)

docx_text = tk.Text(folder_frame, height=1,width=60)
docx_text.pack()
docx_text.insert(tk.END, load_data_path)

update_db_button = tk.Button(folder_frame, text="DB更新", command=update_database)
update_db_button.pack(side=tk.RIGHT, padx=5)

message_frame = tk.Frame(tab2)
message_frame.pack(pady=10)
message_label = tk.Label(message_frame, text="メッセージ")
message_label.pack(anchor=tk.W)
message_text = tk.Text(message_frame, height=10, width=60)
message_text.pack()

# 初期処理後メッセージ
message_text.insert(0.0, init_result + "\n")

# イベントループの開始
tab_control.pack(expand=1, fill='both')
root.mainloop()
