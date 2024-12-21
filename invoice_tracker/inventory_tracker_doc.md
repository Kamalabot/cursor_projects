

Here's the complete markdown document for the inventory tracking application:

```markdown:inventory_tracker.md
# Electronics Inventory Tracking System

A Flask-based inventory management system for electronic components with Bootstrap styling and SQLite database.

## Project Structure
```
electronics_inventory/
    ├── static/
    │   └── css/
    │       └── style.css
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── add_item.html
    │   └── upload_csv.html
    ├── app.py
    ├── database.py
    └── inventory_sample.csv
```

## Installation and Setup

1. Create a new directory for the project:
```bash
mkdir electronics_inventory
cd electronics_inventory
```

2. Install required packages:
```bash
pip install flask
```

3. Create the necessary files and directories as shown in the project structure.

## Database Setup

Create `database.py`:
```python
import sqlite3

def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Create table for electronics inventory
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            category TEXT NOT NULL,
            sector TEXT NOT NULL,
            application TEXT NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
```

## Flask Application

Create `app.py`:
```python
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import csv
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM inventory ORDER BY date_added DESC').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=('GET', 'POST'))
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        category = request.form['category']
        sector = request.form['sector']
        application = request.form['application']
        
        if not name or not quantity:
            flash('Name and quantity are required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO inventory (name, quantity, category, sector, application) VALUES (?, ?, ?, ?, ?)',
                        (name, quantity, category, sector, application))
            conn.commit()
            conn.close()
            flash('Item successfully added!')
            return redirect(url_for('index'))
            
    return render_template('add_item.html')

@app.route('/upload_csv', methods=('GET', 'POST'))
def upload_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(url_for('upload_csv'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('upload_csv'))
        
        if file and file.filename.endswith('.csv'):
            # Read the CSV file
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_data = csv.reader(stream)
            
            conn = get_db_connection()
            success_count = 0
            error_count = 0
            
            for row in csv_data:
                try:
                    # Assuming CSV format: name, quantity, category, sector, application, date
                    name, quantity, category, sector, application, *_ = row
                    
                    conn.execute('''
                        INSERT INTO inventory (name, quantity, category, sector, application)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name.strip(), int(quantity), category.strip(), 
                         sector.strip(), application.strip()))
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    continue
            
            conn.commit()
            conn.close()
            
            flash(f'Successfully imported {success_count} items. {error_count} items failed.')
            return redirect(url_for('index'))
        else:
            flash('Please upload a CSV file')
            return redirect(url_for('upload_csv'))
            
    return render_template('upload_csv.html')

if __name__ == '__main__':
    from database import init_db
    init_db()
    app.run(debug=True)
```

## HTML Templates

### Base Template (`templates/base.html`):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Electronics Inventory</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">Electronics Inventory</a>
            <div class="navbar-nav">
                <a class="nav-link" href="{{ url_for('index') }}">Home</a>
                <a class="nav-link" href="{{ url_for('add_item') }}">Add Item</a>
                <a class="nav-link" href="{{ url_for('upload_csv') }}">Import CSV</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% for message in get_flashed_messages() %}
            <div class="alert alert-info">{{ message }}</div>
        {% endfor %}
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Index Template (`templates/index.html`):
```html
{% extends 'base.html' %}

{% block content %}
    <h1>Inventory List</h1>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Name</th>
                <th>Quantity</th>
                <th>Category</th>
                <th>Sector</th>
                <th>Application</th>
                <th>Date Added</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item['name'] }}</td>
                <td>{{ item['quantity'] }}</td>
                <td>{{ item['category'] }}</td>
                <td>{{ item['sector'] }}</td>
                <td>{{ item['application'] }}</td>
                <td>{{ item['date_added'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}
```

### Add Item Template (`templates/add_item.html`):
```html
{% extends 'base.html' %}

{% block content %}
    <h1>Add New Item</h1>
    <form method="post">
        <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input type="text" class="form-control" id="name" name="name" required>
        </div>
        <div class="mb-3">
            <label for="quantity" class="form-label">Quantity</label>
            <input type="number" class="form-control" id="quantity" name="quantity" required>
        </div>
        <div class="mb-3">
            <label for="category" class="form-label">Category</label>
            <input type="text" class="form-control" id="category" name="category" required>
        </div>
        <div class="mb-3">
            <label for="sector" class="form-label">Sector</label>
            <input type="text" class="form-control" id="sector" name="sector" required>
        </div>
        <div class="mb-3">
            <label for="application" class="form-label">Application</label>
            <textarea class="form-control" id="application" name="application" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Add Item</button>
    </form>
{% endblock %}
```

### CSV Upload Template (`templates/upload_csv.html`):
```html
{% extends 'base.html' %}

{% block content %}
    <h1>Upload Inventory CSV</h1>
    <div class="card mt-4">
        <div class="card-body">
            <h5 class="card-title">CSV Format Requirements</h5>
            <p class="card-text">Please ensure your CSV file follows this format:</p>
            <code>name, quantity, category, sector, application</code>
            <p class="card-text mt-2">Example:</p>
            <code>electronic1, 15, home appliances, Kitchen, Dish Washing</code>
        </div>
    </div>

    <form method="post" enctype="multipart/form-data" class="mt-4">
        <div class="mb-3">
            <label for="file" class="form-label">Select CSV File</label>
            <input type="file" class="form-control" id="file" name="file" accept=".csv" required>
        </div>
        <button type="submit" class="btn btn-primary">Upload and Import</button>
    </form>
{% endblock %}
```

## Sample CSV Data

Create `inventory_sample.csv`:
```csv
LED TV Samsung,25,home appliances,Living Room,Entertainment Display,2024-12-21 16:16:53
Microwave Oven,15,home appliances,Kitchen,Food Heating,2024-12-21 16:17:00
Smart Thermostat,30,home automation,HVAC,Temperature Control,2024-12-21 16:17:15
Security Camera,40,security,Outdoor,Surveillance,2024-12-21 16:17:30
Robot Vacuum,12,home appliances,Cleaning,Floor Cleaning,2024-12-21 16:17:45
Smart Door Lock,20,security,Entry,Access Control,2024-12-21 16:18:00
Air Purifier,18,home appliances,Bedroom,Air Cleaning,2024-12-21 16:18:15
Smart Speaker,50,home automation,Living Room,Voice Control,2024-12-21 16:18:30
Dishwasher,10,home appliances,Kitchen,Dish Cleaning,2024-12-21 16:18:45
Smart Light Bulbs,100,home automation,Lighting,Illumination Control,2024-12-21 16:19:00
```

## Running the Application

1. Make sure all files are created in the correct directory structure
2. Open a terminal in the project directory
3. Run the application:
```bash
python app.py
```
4. Open a web browser and navigate to `http://localhost:5000`

## Features
- View all inventory items
- Add individual items through a web form
- Bulk import items via CSV file
- Bootstrap-styled responsive interface
- SQLite database for data persistence
- Flash messages for user feedback

## Future Enhancements
- Edit functionality
- Delete functionality
- Search and filter capabilities
- User authentication
- Stock alerts
- Export functionality
- Data validation
- Duplicate entry handling
```

This markdown document provides a complete guide to setting up and running the electronics inventory tracking system. You can save this as `inventory_tracker.md` and use it as a reference for implementing the system.
