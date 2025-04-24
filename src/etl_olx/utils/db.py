import os
import sqlite3
from pathlib import Path

# Configurações
DB_FOLDER = "data"
DB_FILENAME = "olx_anuncios.db"
DB_PATH = os.path.join(DB_FOLDER, DB_FILENAME)


def get_connection():
    """Retorna conexão com o banco de dados SQLite local"""
    Path(DB_FOLDER).mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_table_if_needed():
    """Cria a tabela 'anuncios' se não existir"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS anuncios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                preco TEXT,
                link TEXT UNIQUE
            )
        """
        )
        conn.commit()


def ad_exists(link):
    """Verifica se o anúncio já existe no banco"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM anuncios WHERE link = ?", (link,))
        return cursor.fetchone() is not None


def save_ad(title, price, link):
    """Salva um anúncio no banco"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO anuncios (titulo, preco, link) VALUES (?, ?, ?)",
        (title, price, link),
    )
    conn.commit()
    conn.close()
