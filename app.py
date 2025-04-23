from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

def conectar_db():
    return sqlite3.connect("historia_clinica.db")

@app.route('/historia', methods=['POST'])
def agregar_historia():
    data = request.get_json()
    print(data)  # Este print mostrará lo que estás enviando
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historias_clinicas (nombre, dni, fecha_consulta, diagnostico, tratamiento, obra_social)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (data['nombre'], data['dni'], data['fecha'], data['diagnostico'], data['tratamiento'], data['obra_social'])
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Historia guardada"}), 201

@app.route('/historias', methods=['GET'])
def obtener_historias():
    filtro = request.args.get('filtro', '')
    conn = conectar_db()
    cursor = conn.cursor()
    if filtro:
        cursor.execute("""
            SELECT * FROM historias_clinicas
            WHERE nombre LIKE ? OR dni LIKE ? OR fecha_consulta LIKE ?
        """, (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"))
    else:
        cursor.execute("SELECT * FROM historias_clinicas")
    historias = cursor.fetchall()
    conn.close()
    return jsonify(historias)

@app.route('/historia/<int:id>', methods=['DELETE'])
def eliminar_historia(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM historias_clinicas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Historia eliminada"}), 200

@app.route('/historia/<int:id>', methods=['PUT'])
def actualizar_historia(id):
    data = request.get_json()
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE historias_clinicas
        SET nombre = ?, dni = ?, fecha_consulta = ?, diagnostico = ?, tratamiento = ?, obra_social = ?
        WHERE id = ?
    """, (data['nombre'], data['dni'], data['fecha'], data['diagnostico'], data['tratamiento'], data['obra_social'], id))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Historia actualizada"}), 200

def crear_tabla_si_no_existe():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historias_clinicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            dni TEXT,
            fecha_consulta TEXT,
            diagnostico TEXT,
            tratamiento TEXT,
            obra_social TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tabla_si_no_existe()
    port = int(os.environ.get("PORT", 8000))  # Puerto por defecto 8000 si no hay variable PORT
    app.run(host="0.0.0.0", port=port)