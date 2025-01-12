import pandas as pd
from flask import Flask, request, jsonify, send_file
import io
import os
from werkzeug.utils import secure_filename
from project_data_ingestion import clean_project_data
# ... existing clean_project_data function remains unchanged ...

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'X:\\bi_uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process-excel', methods=['GET'])
def process_excel():
    try:
        # Add logging to see what's happening
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request method: {request.method}")
        
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
        print(f"Found files: {files}")
        
        if not files:
            error_msg = 'No Excel files found in the upload folder'
            print(error_msg)
            return jsonify({'error': error_msg}), 400
        
        cleaned_dfs = []
        
        for filename in files:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Processing file: {filepath}")
            cleaned_df = clean_project_data(filepath)
            cleaned_dfs.append(cleaned_df)
            # os.remove(filepath)

        final_cleaned_df = pd.concat(cleaned_dfs, ignore_index=True)
        print(f"Processed {len(cleaned_dfs)} files successfully")

        # Create in-memory copy for response
        output = io.BytesIO()
        final_cleaned_df.to_excel(output, index=False)
        output.seek(0)
        
        # Add CORS headers
        headers = {
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS'
        }
        
        return output.getvalue(), 200, headers
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Add OPTIONS method support for CORS
@app.route('/process-excel', methods=['OPTIONS'])
def options():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return '', 204, headers

if __name__ == '__main__':
    print("Starting server...") 
    app.run(debug=True, host='0.0.0.0', port=5000)