import sqlite3

class Dao():
    def __init__(self):
        # データベースに接続と作成
        dbname = "study_record.db"
        self.connection = sqlite3.connect(dbname)

        # カーソルの取得
        self.c = self.connection.cursor()

        # テーブル作成
        create_ddl = """
        CREATE TABLE IF NOT EXISTS study_records
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        days TEXT,
        item TEXT,
        timer TEXT,
        contents TEXT
        );
        """
        self.c.execute(create_ddl)


    def insert_study_record(self, words = None, dt_now = None, study_item = None, studied_time = None):

        if words != '' or studied_time != '00:00:00':
            rdo_text = {1 : 'Java', 2 : 'Python', 3: 'Unity'}
            # itemテーブル登録のテスト
            self.c.execute('INSERT INTO study_records(days, item, timer, contents) VALUES(?,?,?,?)' , (dt_now, rdo_text[study_item] ,studied_time, words))
            self.c.execute("COMMIT;")


    def show_latest_records(self):
        result = self.c.execute("SELECT days, item, timer, contents FROM study_records ORDER BY id DESC;")
        rows = []
        for row in result:
            rows.append(row)
        return rows
    
    
    def connection_close(self):
        # データベースに変更を保存
        self.connection.commit()
        # データベースを閉じる
        self.connection.close()