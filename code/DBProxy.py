import sqlite3


class DBProxy:
    def __init__(self, db_name: str):
        self.db_name = db_name
        try:
            with sqlite3.connect(db_name) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS dados(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        date TEXT NOT NULL)
                """)
        except sqlite3.Error as e:
            print(f"[ERRO] Erro ao conectar ou criar tabela no banco de dados: {e}")

    def save(self, score_dict: dict):
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("INSERT INTO dados (name, score, date) VALUES (:name, :score, :date)", score_dict)
                conn.commit()
        except sqlite3.Error as e:
            print(f"[ERRO] Erro ao salvar dados no banco de dados: {e}")

    def retrieve_top10(self) -> list:
        try:
            with sqlite3.connect(self.db_name) as conn:
                return conn.execute("SELECT * FROM dados ORDER BY score DESC LIMIT 10").fetchall()
        except sqlite3.Error as e:
            print(f"[ERRO] Erro ao recuperar dados do banco de dados: {e}")
            return []

    def retrieve_all(self) -> list:
        try:
            with sqlite3.connect(self.db_name) as conn:
                return conn.execute("SELECT * FROM dados ORDER BY score DESC").fetchall()
        except sqlite3.Error as e:
            print(f"[ERRO] Erro ao recuperar dados do banco de dados: {e}")
            return []
