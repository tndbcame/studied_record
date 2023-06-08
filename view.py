import datetime
import tkinter as tk
import time

from tkinter.scrolledtext import ScrolledText
from dao import Dao



class View(tk.Frame):


    def getFrame(self):
        """画面レイアウト"""

        #画面部品
        self.show_studied_record_frame = tk.Frame(
            self.master,
            background="#1d2126",
            width=1000,
            height=500 
            )
        record_header = tk.Label(
            self.show_studied_record_frame,
            text = "最新の学習記録を表示",
            font=("Times New Roman", "15", "bold"),
            background="#0161c1",
            foreground='#dce0e4'
            )
        showButton = tk.Button(
            self.show_studied_record_frame,text="再表示",
            font=("Times New Roman", "15", "bold"),
            background ="#ae1934",
            relief = "flat",
            foreground='#dce0e4',
            activeforeground ='#b55e6d',
            activebackground = "#1d2126",
            command= self.show_query
            )
        self.input_studied_fram = tk.Frame(
            self.master,
            background="#1d2126", 
            width=1000, 
            height=225 
            )
        study_record_title = tk.Label(
            self.input_studied_fram,
            text = "学習したことを記入する",
            font=("Times New Roman", "15", "bold"),
            background="#0161c1",
            foreground='#dce0e4'
            )
        study_record_item = tk.Label(
            self.input_studied_fram,
            text = "学習記録した項目を選択",
            font=("Times New Roman", "10", "bold"),
            background="#1d2126",
            foreground='#dce0e4'
            )
        study_record_timer_title = tk.Label(
            self.input_studied_fram,
            text = "学習タイマー",
            font=("Times New Roman", "10", "bold"),
            background="#1d2126",
            foreground='#dce0e4'
            )
        studying_contents = tk.Label(
            self.input_studied_fram,
            text = "学習内容",
            font=("Times New Roman", "10", "bold"),
            background="#1d2126",
            foreground='#dce0e4'
            )
        #TODO:radiobottunをリストとかにしてループで回して作成できるようにする
        self.rdo_grp = tk.IntVar(value = 1)
        rdo1 = tk.Radiobutton(
            self.input_studied_fram, text='Java', 
            value=1, 
            variable=self.rdo_grp, 
            background ="#1d2126",
            font=("Times New Roman", "9", "bold"),
            foreground='#7f5eb5',
            activeforeground ='#b55e6d',
            activebackground = "#1d2126"
            )
        rdo2 = tk.Radiobutton(
            self.input_studied_fram, text='Python', 
            value=2, 
            variable=self.rdo_grp, 
            background ="#1d2126",
            font=("Times New Roman", "9", "bold"),
            foreground='#7f5eb5',
            activeforeground ='#b55e6d',
            activebackground = "#1d2126"
            )
        rdo3 = tk.Radiobutton(
            self.input_studied_fram, text='Unity', 
            value=3, 
            variable=self.rdo_grp, 
            background ="#1d2126",
            font=("Times New Roman", "9", "bold"),
            foreground='#7f5eb5',
            activeforeground ='#b55e6d',
            activebackground = "#1d2126"
            )
        self.input_studied = ScrolledText(
            self.input_studied_fram,
            font =("Times New Roman", "9")
            )
        okButton = tk.Button(
            self.input_studied_fram,text="OK",
            font=("Times New Roman", "15", "bold"),
            background ="#ae1934",
            relief = "flat",
            foreground='#dce0e4',
            activeforeground ='#b55e6d',
            activebackground = "#1d2126",
            command=self.insert_query 
            )
        startButton = tk.Button(
            self.input_studied_fram,text="START",
            relief = tk.SOLID,
            background ="#1d2126",
            font=("Times New Roman", "9", "bold"),
            foreground='#7f5eb5',
            activeforeground ='#b55e6d',
            activebackground = "#1d2126",
            command=self.start,
            width=10
            )
        stopButton = tk.Button(
            self.input_studied_fram,text="STOP",
            relief = tk.SOLID,
            background ="#1d2126",
            font=("Times New Roman", "9", "bold"),
            foreground='#7f5eb5',
            activeforeground ='#b55e6d',
            activebackground = "#1d2126",
            command=self.stop,
            width=10
            )
        self.timerView = tk.Label(
            self.input_studied_fram,
            background ="#1d2126",
            font=("Times New Roman", "42", "bold"),
            foreground='#7f5eb5',
            text="00:00:00"
            )

        #配置
        self.show_studied_record_frame.propagate(False)#packの時有効
        record_header.pack(anchor=tk.NW)
        self.show_studied_record_frame.pack(side = tk.BOTTOM, padx = 50,pady= (0,25))
        showButton.place(x=900, y=15)
        self.input_studied_fram.pack(side = tk.BOTTOM, padx = 50, pady = (25,25))
        self.input_studied_fram.grid_propagate(False)#gridはこれ
        study_record_title.grid(column=0, row=0)
        study_record_item.grid(column=0, row=1, sticky=tk.W, ipadx=15, ipady=15)
        study_record_timer_title.grid(column=0, row=2, sticky=tk.W, padx=15, pady=(20,25))
        studying_contents.grid(column=1, row=1, sticky=tk.W, ipady=15)
        rdo1.place(x=15, y=70)
        rdo2.place(x=63, y=70)
        rdo3.place(x=125, y=70)
        self.input_studied.place(width=740, height=130, x=240, y=70)
        okButton.place(x=933, y=15)
        self.timerView.place(x=11, y=120)
        startButton.place(x=37.5, y=198)
        stopButton.place(x=115.5, y=198)


    def insert_query(self):
        """最新の学習内容を登録"""
        
        #学習項目
        study_item = self.rdo_grp.get()

        #学習内容("end"だと\n 文字も含まれる→"end-1c"は一文字前まで)
        words = self.input_studied.get('1.0','end - 1c')
        self.input_studied.delete('1.0','end - 1c')

        #今日の日付
        dt_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        #勉強時間
        studied_time = self.timerView["text"]
        self.d.insert_study_record(words, dt_now, study_item, studied_time)


    def show_query(self):
        """最新の学習記録を取得"""

        #二回目の呼び出し以降フレームを削除
        if self.count >= 1:
            # self.innerFrame.destroy()
            self.canvas.destroy()
            self.sb.destroy()

        #キャンバス
        self.canvas=tk.Canvas(
            self.show_studied_record_frame,
            background="#355e88",
            relief='flat',
            width=900,
            height=400 
            )
        
        #スクロールバー
        self.sb = tk.Scrollbar(
            self.canvas, 
            orient="vertical", 
            command=self.canvas.yview
            ) 
 
        #インナーフレーム
        self.innerFrame = tk.Frame(
            self.canvas,
            background="#355e88"
            )
        
        #配置
        self.canvas.pack(side = tk.BOTTOM, padx = 50,pady= (0,25))
        self.canvas.propagate(False)
        self.sb.pack(side=tk.RIGHT, fill="y")
        self.canvas.configure(yscrollcommand=self.sb.set) 
        self.canvas.create_window((0,0), window=self.innerFrame, anchor="nw")

        #表示する学習内容を取得する
        result = self.d.show_latest_records()
        for i in range(len(result)):
            record =[]
            record.append(
                "学習日 : " + result[i][0] 
                + "    学習項目 : " + result[i][1] 
                + "    学習時間 : " + result[i][2]
                )
            record.append(result[i][3])
            for n in range(len(record)):
                self.studied_record = tk.Message(
                    self.innerFrame,
                    text = record[n],
                    font=("Times New Roman", "10", "bold"),
                    background="#355e88",
                    foreground='#dce0e4',
                    width=865
                    )
                self.studied_record.pack(anchor=tk.W)

        #呼び出しカウント
        self.count += 1
        
        #フレームの大きさに合わせてキャンバス領域を増やす
        self.innerFrame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"), highlightbackground="#355e88")
        

    def update_time(self):
        """時間更新関数"""
        self.after_id = self.input_studied_fram.after(self.INTERVAL, self.update_time)
        now_time = time.time()
        elapsed_time = now_time - self.start_time
        m, second = divmod(elapsed_time, 60)
        hour, minute = divmod(m, 60)
        self.timerView.config(text= "{0:0=2g}:{1:0=2g}:{2:0=2.0f}".format(hour, minute, second))


    def start(self):
        """計測スタート"""
        if not self.start_flag:
            self.start_flag = True
            self.start_time = time.time()
            self.after_id = self.input_studied_fram.after(self.INTERVAL, self.update_time)

    def stop(self):
        """計測ストップ"""
        if self.start_flag:
            self.input_studied_fram.after_cancel(self.after_id)
            self.start_flag = False


    def __init__(self, master=None):
        """初期処理"""

        #定数、変数定義
        self.INTERVAL = 10
        self.start_flag = False
        self.count = 0
        self.d = Dao()
        
        # Windowの初期設定を行う。
        super().__init__(master)

        # Windowの画面サイズを設定する。
        self.master.geometry("1100x800")
        self.master.configure(bg="#060a0e")

        #フレーム取得
        self.getFrame()

        #DBからレコード取得
        self.show_query()

        #TODO
        #リファクタリングする
        #一時間ごとにポップアップウィンドウ表示する機能を作る