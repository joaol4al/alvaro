from flask import Flask, request, redirect, render_template, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('C:/Users/jv175/Desktop/REDE SOCIAL/banco_de_dados/usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicialização do banco de dados
def init_db():
    banco = get_db_connection()
    cursor = banco.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    
    banco.commit()
    banco.close()

@app.route('/')
def home():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        email = request.form['email']
        senha = request.form['password']

        banco = get_db_connection()
        
        cursor = banco.cursor()
        cursor.execute('INSERT INTO usuarios (nome, sobrenome, telefone, cpf, email, senha) VALUES (?, ?, ?, ?, ?, ?)',
                       (nome, sobrenome, telefone, cpf, email, senha))
        banco.commit()
        
        print("Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: CPF ou email já cadastrados.")
        return "Erro: CPF ou email já cadastrados."
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar: {e}")
        return f"Erro ao cadastrar: {e}"
    finally:
        banco.close()

    return redirect(url_for('home'))

@app.route('/test')
def test():
    return "A rota de teste está funcionando!"

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    app.run(debug=True)
