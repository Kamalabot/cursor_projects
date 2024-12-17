import requests
import sys
import json

def send_csv_for_analysis(file_path: str, server_url: str = "http://localhost:8000"):
    """Send CSV file to server for analysis"""
    
    endpoint = f"{server_url}/analyze-csv/"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'text/csv')}
            response = requests.post(endpoint, files=files)
            
        if response.status_code == 200:
            print("Analysis Results:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <path_to_csv_file>")
        sys.exit(1)
        
    csv_file_path = sys.argv[1]
    send_csv_for_analysis(csv_file_path) 