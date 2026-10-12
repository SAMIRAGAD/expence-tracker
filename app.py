from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_expense, get_all_expenses, group_expenses_by_date, get_total_for_date, delete_expense, get_budget, update_budget
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    expenses = get_all_expenses()
    grouped = group_expenses_by_date(expenses)
    daily_totals = {date: get_total_for_date(exps) for date, exps in grouped.items()}
    
    # Получаем бюджет из базы данных
    budget = get_budget()
    
    # Сегодня
    today = datetime.now().strftime('%Y-%m-%d')
    today_expenses = [e for e in expenses if e['date'] == today]
    daily_total = sum(e['amount'] for e in today_expenses)
    today_count = len(today_expenses)
    
    # Эта неделя
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    week_expenses = [e for e in expenses if e['date'] >= week_ago]
    weekly_total = sum(e['amount'] for e in week_expenses)
    week_count = len(week_expenses)
    
    # Этот месяц
    this_month = datetime.now().strftime('%Y-%m')
    month_expenses = [e for e in expenses if e['date'].startswith(this_month)]
    monthly_total = sum(e['amount'] for e in month_expenses)
    
    # Процент бюджета
    budget_percent = min(int((monthly_total / budget) * 100), 100) if budget > 0 else 0
    
    # Текущая дата и время
    now_date = datetime.now().strftime('%Y-%m-%d')
    now_time = datetime.now().strftime('%H:%M')
    
    return render_template('index.html',
                         grouped_expenses=grouped,
                         daily_totals=daily_totals,
                         daily_total=daily_total,
                         today_count=today_count,
                         weekly_total=weekly_total,
                         week_count=week_count,
                         monthly_total=monthly_total,
                         budget=budget,
                         budget_percent=budget_percent,
                         now_date=now_date,
                         now_time=now_time)

@app.route('/add', methods=['POST'])
def add():
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']
    date = request.form['date']
    time = request.form['time']
    
    add_expense(amount, category, description, date, time)
    return redirect(url_for('index'))

@app.route('/set_budget', methods=['POST'])
def set_budget():
    new_budget = float(request.form['budget'])
    update_budget(new_budget)
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>')
def delete(expense_id):
    delete_expense(expense_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)