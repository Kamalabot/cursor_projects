# HTMX Detailed Task List Implementation Guide

## Overview
This guide explains the implementation of a detailed task list feature using HTMX, Flask, and Bootstrap. The feature adds priority levels, status tracking, and due dates while maintaining the original simple task view.

## New Features Added
- Task Priority (Low, Medium, High)
- Task Status (Pending, In Progress, Completed, On Hold) 
- Target Date
- Detailed View Interface

## Implementation Components

### 1. Backend Routes (app.py)
```python
@app.route('/detailed')
def detailed_index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('detailed_index.html', tasks=tasks)

@app.route('/detailed/tasks', methods=['POST'])
def add_detailed_task():
    # Handle detailed task creation with priority and status
    title = request.form.get('title')
    target_date = request.form.get('target_date')
    priority = request.form.get('priority', 0)
    status = request.form.get('status', 'pending')
    
    # Process and save task
    if title:
        task = Task(
            title=title,
            target_date=target_date,
            priority=priority,
            status=status
        )
        db.session.add(task)
        db.session.commit()
```

### 2. Frontend Templates

#### Detailed Index Page (detailed_index.html)
```html
<form hx-post="/detailed/tasks" hx-target="#detailed-task-list">
    <div class="row g-3">
        <!-- Task Title -->
        <div class="col-md-6">
            <input type="text" name="title" class="form-control" required>
        </div>
        
        <!-- Target Date -->
        <div class="col-md-6">
            <input type="date" name="target_date" class="form-control">
        </div>
        
        <!-- Priority Selection -->
        <div class="col-md-6">
            <select name="priority" class="form-select">
                <option value="0">Low Priority</option>
                <option value="1">Medium Priority</option>
                <option value="2">High Priority</option>
            </select>
        </div>
        
        <!-- Status Selection -->
        <div class="col-md-6">
            <select name="status" class="form-select">
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="on_hold">On Hold</option>
            </select>
        </div>
    </div>
</form>
```

## HTMX Interactions

### 1. Task Creation
```html
<!-- Form submission -->
<form hx-post="/detailed/tasks" hx-target="#detailed-task-list">
```
- Sends POST request to /detailed/tasks
- Updates #detailed-task-list with new content
- No page reload required

### 2. Status Updates
```html
<select hx-post="/tasks/{{ task.id }}/update-status"
        hx-target="#detailed-task-list"
        name="status">
```
- Triggers on select change
- Updates task status immediately
- Refreshes task list with new status

### 3. Priority Updates
```html
<select hx-post="/tasks/{{ task.id }}/update-status"
        hx-target="#detailed-task-list"
        name="priority">
```
- Updates priority level
- Immediate server sync
- Real-time UI update

### 4. Task Editing
```html
<!-- Edit Button Trigger -->
<button class="btn btn-secondary btn-sm"
        hx-get="/tasks/{{ task.id }}/edit"
        hx-target="#task-{{ task.id }}">
    <i class="bi bi-pencil"></i> Edit
</button>
```
- Triggers inline edit form
- Targets specific task by ID
- Smooth transition to edit mode

#### Edit Form Template (edit_task.html)
```html
<form hx-post="/tasks/{{ task.id }}/edit" hx-target="#task-{{ task.id }}">
    <div class="row g-3">
        <div class="col-md-6">
            <input type="text" name="title" value="{{ task.title }}" required>
        </div>
        <div class="col-md-6">
            <input type="date" name="target_date" 
                   value="{{ task.target_date.strftime('%Y-%m-%d') if task.target_date }}">
        </div>
        <!-- Priority and Status dropdowns -->
        <div class="col-12">
            <button type="submit">Save Changes</button>
            <button hx-get="/tasks/{{ task.id }}/view">Cancel</button>
        </div>
    </div>
</form>
```

#### Backend Route for Editing
```python
@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.target_date = datetime.strptime(request.form.get('target_date'), '%Y-%m-%d') \
                          if request.form.get('target_date') else None
        task.priority = int(request.form.get('priority', 0))
        task.status = request.form.get('status', 'pending')
        
        db.session.commit()
        return render_template('partials/task_list_with_status.html', tasks=Task.query.all())
    
    return render_template('partials/edit_task.html', task=task)
```

### Edit Feature Benefits
- Inline editing without page reload
- Pre-filled form with current values
- Cancel option to revert changes
- Immediate UI update after save
- Maintains task list context

### Edit Workflow
1. Click edit button → Shows edit form
2. Modify task details → Submit form
3. Server processes changes → Updates database
4. Returns updated view → HTMX updates DOM
5. Cancel returns to view mode → No changes saved

## Data Flow

1. **Task Creation:**
   - User fills form
   - HTMX sends POST request
   - Server creates task
   - Returns updated task list
   - HTMX updates DOM

2. **Status/Priority Updates:**
   - User changes dropdown
   - HTMX sends POST request
   - Server updates database
   - Returns fresh task list
   - HTMX updates view

## Best Practices

### 1. Form Organization
- Group related fields
- Use Bootstrap grid system
- Clear visual hierarchy

### 2. HTMX Targeting
- Specific target IDs
- Partial template updates
- Efficient DOM manipulation

### 3. Status Management
- Consistent status options
- Clear visual indicators
- Immediate feedback

## Navigation Integration
```html
<nav class="navbar navbar-dark bg-dark">
    <div class="container">
        <a href="/" class="btn btn-outline-light">Simple View</a>
        <a href="/detailed" class="btn btn-outline-light">Detailed View</a>
    </div>
</nav>
```

## Error Handling
- Form validation
- Required fields
- Date format validation
- Status/priority constraints

## Future Enhancements
1. Task categories
2. Priority color coding
3. Due date notifications
4. Status transition rules
5. Task dependencies

## Resources
- [HTMX Documentation](https://htmx.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
```

This markdown file provides:
- Detailed implementation steps
- Code examples with explanations
- Data flow descriptions
- Best practices
- Future enhancement possibilities
- Relevant documentation links