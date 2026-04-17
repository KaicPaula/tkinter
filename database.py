import sqlite3
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
        

        
    
    
