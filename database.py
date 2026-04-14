import sqlite3
def inicializar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS nomes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_entrada TEXT NOT NULL
                )""")

    conexao.commit()
    conexao.close()