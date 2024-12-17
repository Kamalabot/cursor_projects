from flask import Flask, request, render_template
import pandas as pd
import io

app = Flask(__name__)

def analyze_csv(df: pd.DataFrame) -> dict:
    """Perform basic analysis on the CSV data"""
    analysis = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_columns_stats": df.describe().to_dict(),
    }
    return analysis

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        
        if file.filename == '':
            return "No selected file"
        
        if not file.filename.endswith('.csv'):
            return "File must be a CSV"
        
        # Read the CSV file
        contents = file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Perform analysis
        results = analyze_csv(df)
        return render_template('results.html', results=results)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True) 