import sqlite3
from datetime import datetime

DB_NAME = 'expenses.db'

def init_db():
    """Создаём таблицы"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица расходов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    
    # Таблица настроек (для бюджета)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value REAL NOT NULL
        )
    ''')
    
    # Устанавливаем бюджет по умолчанию, если его нет
    cursor.execute('''
        INSERT OR IGNORE INTO settings (key, value) VALUES ('budget', 20000)
    ''')
    
    conn.commit()
    conn.close()

def get_budget():
    """Получаем текущий бюджет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = 'budget'")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 20000

def update_budget(new_budget):
    """Обновляем бюджет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE settings SET value = ? WHERE key = 'budget'",
        (new_budget,)
    )
    conn.commit()
    conn.close()

def add_expense(amount, category, description, date, time):
    """Добавляем новый расход"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO expenses (amount, category, description, date, time) VALUES (?, ?, ?, ?, ?)',
        (amount, category, description, date, time)
    )
    conn.commit()
    conn.close()

def get_all_expenses():
    """Получаем все расходы"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC, time DESC')
    rows = cursor.fetchall()
    conn.close()
    
    expenses = []
    for row in rows:
        expenses.append({
            'id': row[0],
            'amount': row[1],
            'category': row[2],
            'description': row[3],
            'date': row[4],
            'time': row[5]
        })
    return expenses

def group_expenses_by_date(expenses):
    """Группируем расходы по датам"""
    grouped = {}
    for expense in expenses:
        date = expense['date']
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(expense)
    return grouped

def get_total_for_date(expenses):
    """Считаем сумму за день"""
    return sum(exp['amount'] for exp in expenses)

def delete_expense(expense_id):
    """Удаляем расход"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()