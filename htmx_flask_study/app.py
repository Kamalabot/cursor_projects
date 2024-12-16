from flask import Flask, render_template, request, jsonify
from database import db, Task
from datetime import datetime
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
    target_date = request.form.get('target_date')
    target_date = datetime.strptime(target_date, '%Y-%m-%d') if target_date else None
    if title:
        task = Task(title=title, target_date=target_date)
        db.session.add(task)
        db.session.commit()
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    # tasks is the data that goes into the task_list.html file
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

@app.route('/detailed')
def detailed_index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('detailed_index.html', tasks=tasks)

@app.route('/detailed/tasks', methods=['POST'])
def add_detailed_task():
    title = request.form.get('title')
    target_date = request.form.get('target_date')
    priority = request.form.get('priority', 0)
    status = request.form.get('status', 'pending')
    
    target_date = datetime.strptime(target_date, '%Y-%m-%d') if target_date else None
    
    if title:
        task = Task(
            title=title,
            target_date=target_date,
            priority=priority,
            status=status
        )
        db.session.add(task)
        db.session.commit()
    
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('partials/task_list_with_status.html', tasks=tasks)

@app.route('/tasks/<int:task_id>/update-status', methods=['POST'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    status = request.form.get('status')
    priority = request.form.get('priority')
    
    if status:
        task.status = status
    if priority:
        task.priority = int(priority)
    
    db.session.commit()
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('partials/task_list_with_status.html', tasks=tasks)

# need to render template for all the partial update 
# being done on the index.html file
if __name__ == '__main__':
    app.run(debug=True)