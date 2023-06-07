import tkinter as tk
from view import View

#Pythonファイルが「pythonファイル名.py」という形で実行されているか←インポートしただけで実行されないようにする
if __name__ == "__main__":
    # Window生成
    root = tk.Tk()
    root.title("study_record")
    app = View(master=root)
    

    # Windowループ
    app.mainloop()