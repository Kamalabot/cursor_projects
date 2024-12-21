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
