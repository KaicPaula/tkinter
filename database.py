import sqlite3
import datetime



def inicializar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    cargo TEXT -- 'Dono' ou 'Vendedor'
    )
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cor TEXT NOT NULL,
    ano TEXT NOT NULL,
    valor_fipe FLOAT,
    valor_compra_ou_cliente FLOAT, -- O que a loja pagou ou o cliente da revenda quer
    comissao_sugerida FLOAT,
    status TEXT DEFAULT 'Disponível' -- 'Disponível' ou 'Vendido'
)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_veiculo INTEGER NOT NULL,
    id_vendedor INTEGER NOT NULL,
    valor_de_compra_ou_cliente FLOAT NOT NULL,
    valor_final_venda FLOAT NOT NULL,
    data_venda TEXT,
    FOREIGN KEY (id_veiculo) REFERENCES veiculos (id),
    FOREIGN KEY (id_vendedor) REFERENCES funcionarios (id)
)""")

    conexao.commit()
    conexao.close()

class NovoVeiculo:
    def __init__(self,nome, cor, ano, valor_fipe, valor_compra_ou_cliente, comissao_sugerida, status):
        self.nome = nome
        self.cor = cor
        self.ano = ano
        self.valor_fipe = valor_fipe
        self.valor_compra_ou_cliente = valor_compra_ou_cliente
        self.comissao_sugerida = comissao_sugerida
        self.status = status
        
class NovoFuncionario:
    def __init__(self, nome, senha, cargo):
        self.nome = nome
        self.senha = senha
        self.cargo = cargo
        
    def salvar_funcionario_db(self):
        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()
        dados = (
            self.nome,
            self.senha,
            self.cargo
        )
        cursor.execute("""INSERT INTO funcionarios
                       (nome, senha, cargo) VALUES
                       (?,?,?)""", dados)
        conexao.commit()
        
def consultar_login(nome_login, senha_login):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("""SELECT nome, senha FROM funcionarios WHERE nome = ?""",(nome_login,))
    dados = cursor.fetchone()
    if dados == None:
        return None
    elif dados[1] != senha_login:
        return False
    elif dados[0] == nome_login and dados[1] == senha_login:
        return True
    # se o nome existe no banco de dados retorna None
    # se a senha nao coincide retorna False
    # Se os dados  forem exato, retorna True
    
def consultar_cargo(nome_login): 
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("""SELECT cargo FROM funcionarios WHERE nome = ?""",(nome_login,))
    dados = cursor.fetchone()
    if dados[0] == 'vendedor':
        return False
    elif dados[0] == 'gerente' or dados[0] == 'dono':
        return True
    # consultar e validar cargo atual
    
    
def get_conexao():
    return sqlite3.connect("banco.db")

def salvar_veiculo(nome, cor, ano, valor_fipe, valor_compra, comissao):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("""INSERT INTO veiculos (nome, cor, ano, valor_fipe, valor_compra_ou_cliente, comissao_sugerida, status)
                VALUES (?,?,?,?,?,?,?)""", (nome, cor, ano, valor_fipe, valor_compra, comissao, 'disponivel'))
    con.commit()
    con.close()

def deletar_veiculo(id_veiculo):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("DELETE FROM veiculos WHERE id = ?", (id_veiculo,))
    con.commit()
    con.close()

def deletar_funcionario(id_func):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("DELETE FROM funcionarios WHERE id = ?", (id_func,))
    con.commit()
    con.close()

def buscar_veiculo_por_id(id_veiculo):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("SELECT id, nome, cor, ano, valor_fipe, valor_compra_ou_cliente, comissao_sugerida, status FROM veiculos WHERE id = ?", (id_veiculo,))
    resultado = cur.fetchone()
    con.close()
    return resultado

def listar_veiculos(apenas_disponiveis=False):
    con = get_conexao()
    cur = con.cursor()
    if apenas_disponiveis:
        cur.execute("SELECT id, nome, cor, ano, valor_fipe, valor_compra_ou_cliente, comissao_sugerida, status FROM veiculos WHERE status = 'disponivel'")
    else:
        cur.execute("SELECT id, nome, cor, ano, valor_fipe, valor_compra_ou_cliente, comissao_sugerida, status FROM veiculos")
    resultado = cur.fetchall()
    con.close()
    return resultado

def listar_funcionarios():
    con = get_conexao()
    cur = con.cursor()
    cur.execute("SELECT id, nome, cargo FROM funcionarios")
    resultado = cur.fetchall()
    con.close()
    return resultado

def buscar_funcionario_por_id(id_func):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("SELECT id, nome, cargo FROM funcionarios WHERE id = ?", (id_func,))
    resultado = cur.fetchone()
    con.close()
    return resultado

def buscar_id_funcionario(nome):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("SELECT id FROM funcionarios WHERE nome = ?", (nome,))
    resultado = cur.fetchone()
    con.close()
    return resultado[0]

def get_cargo_texto(nome):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("SELECT cargo FROM funcionarios WHERE nome = ?", (nome,))
    resultado = cur.fetchone()
    con.close()
    return resultado[0]

def verificar_senha_atual(nome):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("SELECT senha FROM funcionarios WHERE nome = ?", (nome,))
    resultado = cur.fetchone()
    con.close()
    return resultado[0]

def alterar_senha_db(nome, nova_senha):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("UPDATE funcionarios SET senha = ? WHERE nome = ?", (nova_senha, nome))
    con.commit()
    con.close()

def realizar_venda_db(id_veiculo, nome_vendedor, valor_final):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("SELECT valor_compra_ou_cliente FROM veiculos WHERE id = ?", (id_veiculo,))
    valor_compra = cur.fetchone()[0]
    id_vendedor = buscar_id_funcionario(nome_vendedor)
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
    cur.execute("UPDATE veiculos SET status = 'indisponivel' WHERE id = ?", (id_veiculo,))
    cur.execute("""INSERT INTO vendas (id_veiculo, id_vendedor, valor_de_compra_ou_cliente, valor_final_venda, data_venda)
                VALUES (?,?,?,?,?)""", (id_veiculo, id_vendedor, valor_compra, valor_final, data_atual))
    con.commit()
    con.close()

def ganhos_todos():
    con = get_conexao()
    cur = con.cursor()
    cur.execute("""SELECT funcionarios.nome, SUM(vendas.valor_final_venda), COUNT(vendas.id)
                   FROM vendas INNER JOIN funcionarios ON vendas.id_vendedor = funcionarios.id
                   GROUP BY vendas.id_vendedor""")
    resultado = cur.fetchall()
    con.close()
    return resultado

def ganhos_vendedor(nome):
    con = get_conexao()
    cur = con.cursor()
    cur.execute("""SELECT funcionarios.nome, SUM(vendas.valor_final_venda), COUNT(vendas.id)
                   FROM vendas INNER JOIN funcionarios ON vendas.id_vendedor = funcionarios.id
                   WHERE funcionarios.nome = ?
                   GROUP BY vendas.id_vendedor""", (nome,))
    resultado = cur.fetchone()
    con.close()
    return resultado


        
    
    
