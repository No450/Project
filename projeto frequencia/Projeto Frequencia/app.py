from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'registro_frequencia',
    'raise_on_warnings': True
}


# Conexão ao banco de dados
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/frequencia', methods=['POST'])
def frequencia():
    matricula = request.form['matricula']
    senha = request.form['senha']
    curso = request.form['curso']
    cursor.execute("SELECT nome FROM alunos WHERE matricula=%s AND senha=%s", (matricula, senha))
    result = cursor.fetchone()
    if result:
        nome = result[0]
        cursor.execute("INSERT INTO frequencia (matricula, data, hora, curso) VALUES (%s, CURDATE(), CURTIME(), %s)", (matricula, curso))
        conn.commit()
        cursor.execute("SELECT * FROM frequencia WHERE matricula=%s", (matricula,))
        frequencias = cursor.fetchall()
        return render_template('frequencia.html', nome=nome, frequencias=frequencias)
    else:
        error = "Matrícula e/ou senha incorretas"
        return render_template('formulario.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
