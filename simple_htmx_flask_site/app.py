from flask import Flask, render_template, request
from datetime import datetime
from dateutil import parser

app = Flask(__name__)

# In-memory storage for tasks (replace with database in production)
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add-task', methods=['POST'])
def add_task():
    task = {
        'id': len(tasks) + 1,
        'title': request.form['title'],
        'priority': request.form['priority'],
        'due_date': parser.parse(request.form['due_date']).date(),
        'completed': False
    }
    tasks.append(task)
    return render_template('task_list.html', tasks=tasks)

@app.route('/update-task', methods=['POST'])
def update_task():
    task_id = int(request.form['id'])
    field = request.form['field']
    value = request.form['value']
    
    for task in tasks:
        if task['id'] == task_id:
            if field == 'priority':
                task[field] = value
            elif field == 'due_date':
                task[field] = parser.parse(value).date()
            elif field == 'completed':
                task[field] = value == 'true'
            break
    
    return render_template('task_list.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
