from flask import Flask, render_template, request, jsonify
from database import db, Task, Category
from datetime import datetime, timezone
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

@app.route('/tasks/today')
def today_tasks():
    today = datetime.now(timezone.utc).date()
    tasks = Task.query.filter(
        db.func.date(Task.target_date) == today
    ).order_by(Task.priority.desc()).all()
    return render_template('partials/task_list_with_status.html', tasks=tasks)

@app.route('/tasks/upcoming')
def upcoming_tasks():
    today = datetime.now(timezone.utc).date()
    tasks = Task.query.filter(
        Task.target_date > today
    ).order_by(Task.target_date.asc()).all()
    return render_template('partials/task_list_with_status.html', tasks=tasks)

@app.route('/tasks/priority')
def priority_tasks():
    tasks = Task.query.filter(
        Task.priority > 0
    ).order_by(Task.priority.desc()).all()
    return render_template('partials/task_list_with_status.html', tasks=tasks)

@app.route('/categories/manage')
def manage_categories():
    return render_template('partials/manage_categories.html', categories=Category.query.all())

@app.route('/tasks/category/<int:category_id>')
def category_tasks(category_id):
    tasks = Task.query.filter_by(category_id=category_id).order_by(Task.created_at.desc()).all()
    return render_template('partials/task_list_with_status.html', tasks=tasks)

# This context processor makes the 'categories' variable available to all templates
# automatically without having to pass it explicitly in each route.
# It queries all categories from the database and injects them into the template context,
# which is particularly useful for rendering the sidebar navigation that shows all categories
@app.context_processor
def inject_categories():
    return dict(categories=Category.query.all())

@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        if request.form.get('target_date'):
            task.target_date = datetime.strptime(request.form.get('target_date'), '%Y-%m-%d')
        task.priority = int(request.form.get('priority', 0))
        task.status = request.form.get('status', 'pending')
        
        db.session.commit()
        return render_template('partials/task_list_with_status.html', tasks=[task])
    
    return render_template('partials/edit_task.html', task=task)

@app.route('/tasks/<int:task_id>/view')
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('partials/task_list_with_status.html', tasks=[task])

@app.route('/categories/add', methods=['POST'])
def add_category():
    name = request.form.get('name')
    color = request.form.get('color', '#000000')
    
    if name:
        category = Category(name=name, color=color)
        db.session.add(category)
        db.session.commit()
    
    return render_template('partials/sidebar.html')

@app.route('/categories/<int:category_id>/delete', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    
    return render_template('partials/sidebar.html')

# need to render template for all the partial update 
# being done on the index.html file
if __name__ == '__main__':
    app.run(debug=True)