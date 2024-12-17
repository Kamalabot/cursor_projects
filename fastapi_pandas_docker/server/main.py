from fastapi import FastAPI, UploadFile, File
import pandas as pd
from typing import Dict
import io

app = FastAPI()

def analyze_csv(df: pd.DataFrame) -> Dict:
    """Perform basic analysis on the CSV data"""
    analysis = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_columns_stats": df.describe().to_dict(),
    }
    return analysis

@app.post("/analyze-csv/")
async def analyze_csv_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return {"error": "File must be a CSV"}
    
    # Read the CSV file
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    # Perform analysis
    results = analyze_csv(df)
    return results 