from flask import Flask, render_template, request, jsonify
from database import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        task = Task(title=title)
        db.session.add(task)
        db.session.commit()
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('partials/task_list.html', tasks=tasks)

@app.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('partials/task_list.html', tasks=tasks)

@app.route('/tasks/<int:task_id>/delete', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('partials/task_list.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)