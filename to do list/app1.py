import sqlite3

from Demos.win32ts_logoff_disconnected import session
from flask import Flask, render_template, url_for ,request
from werkzeug.utils import redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

#web home route
@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html',tasks = tasks)

#route for tasks
@app.route('/add',methods = ['POST'])
def add():
    task = request.form['task']
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks(task) VALUES (?)',(task,))
    conn.commit()
    conn.close()
    return  redirect(url_for('index'))
#for delete task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?',(task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)