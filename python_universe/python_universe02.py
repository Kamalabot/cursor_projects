from pywebio.input import *
from pywebio.output import *
from pywebio.platform.tornado import start_server
import plotly.graph_objects as go
import plotly.utils
import json

from pywebio.input import *
from pywebio.output import *
from pywebio.platform.tornado import start_server
import plotly.graph_objects as go
import requests
import json
from bs4 import BeautifulSoup
import concurrent.futures
import yaml
from pywebio.session import hold

def fetch_awesome_python():
    """Fetch package data from awesome-python GitHub repository"""
    print("Entering fetch_awesome_python")
    try:
        url = "https://raw.githubusercontent.com/vinta/awesome-python/master/README.md"
        response = requests.get(url)
        content = response.text
    except Exception as e:
        print(f"Failed to fetch awesome-python data: {e}")
        return {}
    
    # Parse the markdown content
    sections = {}
    current_section = None
    
    for line in content.split('\n'):
        if line.startswith('## '):
            current_section = line[3:].strip()
            sections[current_section] = []
        elif line.startswith('* [') and current_section:
            # Extract package name from markdown link
            package_name = line.split('[')[1].split(']')[0]
            sections[current_section].append(package_name)
    
    return sections

def fetch_pypi_stats(package_name):
    """Fetch package information from PyPI"""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def group_sections(sections):
    """Group awesome-python sections into broader application domains"""
    print("Entering group_sections to group sections")
    domain_mapping = {
        "Enterprise Solutions": {
            "patterns": [
                "Admin Panels", "CMS", "ERP", "Forms", "Enterprise Applications",
                "Business Intelligence", "RESTful API", "Authentication", "OAuth",
                "Permissions", "CRM", "BPM"
            ],
            "sections": []
        },
        "Web Development": {
            "patterns": [
                "Web Frameworks", "WebSocket", "HTTP", "URL", "HTML", "CSS", 
                "Web Crawling", "Web Content Extracting", "Web Cache",
                "Asynchronous", "WSGI Servers", "Template Engine"
            ],
            "sections": []
        },
        "Data Science & Analytics": {
            "patterns": [
                "Data Analysis", "Data Visualization", "Machine Learning",
                "Deep Learning", "Scientific Computing", "Statistics",
                "Data Validation", "DataFrame", "Neural Network"
            ],
            "sections": []
        },
        "Database & Storage": {
            "patterns": [
                "Database", "Database Drivers", "ORM", "NoSQL", "Caching",
                "Queue", "Storage", "CSV", "Serialization"
            ],
            "sections": []
        },
        "DevOps & Infrastructure": {
            "patterns": [
                "DevOps", "Command-line", "CLI", "Shell", "Terminal",
                "Monitoring", "Logging", "Testing", "CI/CD", "Deployment",
                "Package Management", "Build Tools", "Container"
            ],
            "sections": []
        },
        "Security & Cryptography": {
            "patterns": [
                "Cryptography", "Security", "Authentication", "Passwords",
                "Encryption", "Permission"
            ],
            "sections": []
        },
        "System Integration": {
            "patterns": [
                "Files", "Processes", "Stream", "Concurrency", "Networking",
                "RPC", "Event", "Job Scheduler", "Foreign Function Interface"
            ],
            "sections": []
        },
        "Content Management": {
            "patterns": [
                "Text Processing", "Markdown", "Documentation", "PDF",
                "E-mail", "SMS", "Audio", "Video", "Image Processing",
                "OCR", "Parsing"
            ],
            "sections": []
        },
        "GUI & Desktop": {
            "patterns": [
                "GUI", "Desktop", "Game Development", "Computer Vision",
                "Qt", "Tkinter", "Curses"
            ],
            "sections": []
        },
        "Cloud & Serverless": {
            "patterns": [
                "AWS", "Azure", "Google Cloud", "Cloud", "Serverless",
                "Platform-as-a-Service", "Function-as-a-Service"
            ],
            "sections": []
        }
    }

    # Group sections into domains
    for section_name, packages in sections.items():
        assigned = False
        for domain, info in domain_mapping.items():
            if any(pattern.lower() in section_name.lower() for pattern in info["patterns"]):
                info["sections"].append({
                    "name": section_name,
                    "packages": packages
                })
                assigned = True
                break
        
        if not assigned:
            if "Miscellaneous" not in domain_mapping:
                domain_mapping["Miscellaneous"] = {
                    "patterns": [],
                    "sections": []
                }
            domain_mapping["Miscellaneous"]["sections"].append({
                "name": section_name,
                "packages": packages
            })
    
    # Convert to final format for python_universe
    grouped_universe = {}
    for domain, info in domain_mapping.items():
        if info["sections"]:  # Only include domains that have sections
            domain_packages = []
            for section in info["sections"]:
                domain_packages.extend(section["packages"])
            grouped_universe[domain] = list(set(domain_packages))  # Remove duplicates
    
    return grouped_universe, domain_mapping

def create_python_universe():
    """Create and return the Python universe dictionary and domain mapping"""
    # print("Entering create_python_universe")
    try:
        # First try to load from cache
        with open('python_universe_cache.json', 'r') as f:
            data = json.load(f)
            return data['universe'], data['mapping']
    except Exception as e:
        print("Cache not found, fetching fresh data")
        # Fetch fresh data if cache doesn't exist
        sections = fetch_awesome_python()
        
        # Group sections into broader domains
        python_universe, domain_mapping = group_sections(sections)
        
        # Cache the results
        with open('python_universe_cache.json', 'w') as f:
            json.dump({
                'universe': python_universe,
                'mapping': domain_mapping
            }, f)
        
        return python_universe, domain_mapping
def home_page():
    """Home page with treemap visualization"""
    put_markdown("# Welcome to the Python Universe")
    try:
        python_universe, domain_mapping = create_python_universe()
        # put_text("python_universe is ready")
    except Exception as e:
        print(f"Failed to fetch online data: {e}")
        python_universe = {}
        domain_mapping = {}

    # Create treemap visualization
    put_markdown("## Python Domain Mapping")
    treemap_data = []
    for domain, info in domain_mapping.items():
        treemap_data.append(dict(
            ids=domain,
            labels=domain,
            parents='',
            values=len(info['sections']) if info['sections'] else 0
        ))
        
        for section in info['sections']:
            section_id = f"{domain}/{section['name']}"
            treemap_data.append(dict(
                ids=section_id,
                labels=section['name'],
                parents=domain,
                values=len(section['packages'])
            ))
    
    fig_map = go.Figure(go.Treemap(
        ids=[item['ids'] for item in treemap_data],
        labels=[item['labels'] for item in treemap_data],
        parents=[item['parents'] for item in treemap_data],
        values=[item['values'] for item in treemap_data],
        textinfo="label+value",
        marker=dict(
            colors=[
                'rgb(144, 238, 144)',  # Light green
                'rgb(135, 206, 235)',  # Sky blue
                'rgb(255, 152, 0)',    # Orange
                'rgb(255, 111, 0)',    # Dark orange
                'rgb(255, 87, 34)',    # Deep orange
            ] * (len(treemap_data) // 5 + 1),
            line=dict(
                color='rgb(33, 33, 33)',
                width=2
            )
        ),
        hovertemplate='<b>%{label}</b><br>Packages: %{value}<extra></extra>',
        textfont=dict(
            size=14,
            family='Arial Black, sans-serif',
            color='rgb(33, 33, 33)'
        )
    ))
    
    fig_map.update_layout(
        title=dict(
            text="Python Domain Hierarchy",
            font=dict(
                size=24,
                family='Arial Black, sans-serif',
                color='rgb(33, 33, 33)'
            )
        ),
        height=800,
        margin=dict(t=50, l=25, r=25, b=25)
    )
    
    html_map = fig_map.to_html(include_plotlyjs="require", full_html=False)
    put_html(f"""
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <div class='treemap-container'>
            {html_map}
        </div>
    """)

    # Add styled link to domain selection page
    put_html("""
        <style>
        .nav-link {
            display: inline-block;
            margin: 20px 0;
            padding: 12px 24px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            font-family: 'Arial Black', sans-serif;
            text-align: center;
            transition: background-color 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .nav-link:hover {
            background-color: #45a049;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        </style>
    """)
    
    put_link('Explore Python Domains →', url='/domain_selection', new_window=True)
    
    hold()  # Keep the session alive

def domain_selection():
    """Domain selection page"""
    put_html("""
        <style>
        /* Material Design Typography and Global Styles */
        body {
            font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            background-color: #f5f5f5;
            color: rgba(0, 0, 0, 0.87);
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 500;
            margin-bottom: 1.5rem;
            color: rgba(0, 0, 0, 0.87);
        }
        
        h2 {
            font-size: 2rem;
            font-weight: 500;
            margin-bottom: 1.2rem;
            color: rgba(0, 0, 0, 0.87);
        }
        
        .select-box {
            width: 100%;
            padding: 24px;
            background-color: #ffffff;
            border-radius: 12px;
            margin: 24px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        select[multiple] {
            width: 100%;
            min-height: 400px !important;
            padding: 16px;
            border: 1px solid rgba(0, 0, 0, 0.12);
            border-radius: 8px;
            font-size: 1.1rem;
            font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
        }
        
        option {
            padding: 12px;
            margin: 4px 0;
            border-radius: 6px;
            font-size: 1.1rem;
            transition: background-color 0.2s;
        }
        
        option:checked {
            background-color: #e3f2fd;
            color: #1976D2;
            font-weight: 500;
        }
        
        .package-section {
            margin-top: 48px;
            padding: 24px;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        table {
            font-size: 1.1rem;
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }
        
        td, th {
            padding: 16px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        }
        
        .collapse-header {
            font-size: 1.3rem;
            font-weight: 500;
            padding: 16px;
            background-color: #f5f5f5;
            border-radius: 8px;
            margin: 8px 0;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .collapse-header:hover {
            background-color: #eeeeee;
        }
        
        .nav-button {
            display: inline-block;
            margin: 24px 0;
            padding: 16px 32px;
            background-color: #2196F3;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            font-size: 1.2rem;
            font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 3px 5px rgba(0,0,0,0.2);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .nav-button:hover {
            background-color: #1976D2;
            box-shadow: 0 6px 10px rgba(0,0,0,0.3);
            transform: translateY(-1px);
        }
        
        .section-divider {
            margin: 48px 0;
            border-top: 2px solid rgba(0, 0, 0, 0.08);
        }
        </style>
    """)
    
    put_markdown("# Python Domain Explorer")
    
    try:
        python_universe, _ = create_python_universe()
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        python_universe = {}

    put_html("<div class='select-box'>")
    selected_domains = select(
        label="Select Domains to Explore",
        options=list(python_universe.keys()),
        multiple=True,
        value=list(python_universe.keys()),
        help_text="Hold Ctrl/Cmd to select multiple domains"
    )
    put_html("</div>")
    
    if not selected_domains:
        selected_domains = list(python_universe.keys())
    
    # Filter and show domains in a new section
    filtered_universe = {k: python_universe[k] for k in selected_domains}
    
    put_html("<div class='package-section'>")
    put_markdown("## Python Domains and Packages")
    
    for domain, packages in filtered_universe.items():
        put_collapse(f"{domain} ({len(packages)} packages)", [
            put_table([
                [package] for package in packages
            ])
        ])
    put_html("</div>")
    # Package selection interface
    put_markdown("## Select Packages You've Spiked")
    
    user_packages = []
    for domain, packages in filtered_universe.items():
        domain_selections = checkbox(
            label=domain,
            options=packages,
            value=[]
        )
        user_packages.extend(domain_selections)
    
    # Modified statistics and visualization section
    domain_stats = {domain: len(packages) for domain, packages in filtered_universe.items()}
    
    # Calculate user package stats per domain
    user_domain_stats = {}
    for domain, packages in filtered_universe.items():
        user_domain_stats[domain] = len([pkg for pkg in user_packages if pkg in packages])
    
    # Create and display Plotly bar chart
    put_markdown("## Domain Knowledge Statistics")
       
    # Grouped Bar Chart with brighter colors and larger fonts
    fig = go.Figure(data=[
        go.Bar(
            name='Available Packages',
            x=list(domain_stats.keys()),
            y=list(domain_stats.values()),
            text=list(domain_stats.values()),
            textposition='auto',
            textfont=dict(
                size=16,
                family='Arial Black, sans-serif'
            ),
            marker_color='rgb(100, 255, 100)'  # Brighter green
        ),
        go.Bar(
            name='Packages You Know',
            x=list(user_domain_stats.keys()),
            y=list(user_domain_stats.values()),
            text=list(user_domain_stats.values()),
            textposition='auto',
            textfont=dict(
                size=16,
                family='Arial Black, sans-serif'
            ),
            marker_color='rgb(100, 200, 255)'  # Brighter blue
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Packages by Domain: Available vs. Known",
            font=dict(
                size=24,
                family='Arial Black, sans-serif',
                color='rgb(33, 33, 33)'
            )
        ),
        xaxis_title=dict(
            text="Domains",
            font=dict(
                size=18,
                family='Arial Black, sans-serif'
            )
        ),
        yaxis_title=dict(
            text="Number of Packages",
            font=dict(
                size=18,
                family='Arial Black, sans-serif'
            )
        ),
        height=800,
        barmode='group',
        xaxis={'tickangle': 45, 'tickfont': {'size': 14, 'family': 'Arial Black'}},
        yaxis={'tickfont': {'size': 14, 'family': 'Arial Black'}},
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            font=dict(
                size=16,
                family='Arial Black, sans-serif'
            )
        ),
        margin=dict(b=100)  # Increase bottom margin for rotated labels
    )
    
    html_bar = fig.to_html(include_plotlyjs="require", full_html=False)
    put_html(f"""
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        {html_bar}
    """)
    
    # Show user selection summary
    if user_packages:
        put_markdown("## Your Package Experience")
        put_text(f"You have experience with {len(user_packages)} packages:")
        
        # Group user packages by domain
        user_packages_by_domain = {}
        for domain, packages in filtered_universe.items():
            domain_packages = [pkg for pkg in user_packages if pkg in packages]
            if domain_packages:
                user_packages_by_domain[domain] = domain_packages
        
        # Display packages grouped by domain
        for domain, packages in user_packages_by_domain.items():
            put_collapse(f"{domain} ({len(packages)} packages)", [
                put_table([
                    [package] for package in packages
                ])
            ])
    # Add link back to home
    put_html("""
        <div style="text-align: center; margin-top: 32px;">
            <a href="/" class="nav-button">← Back to Overview</a>
        </div>
    """)
    
    hold()

if __name__ == '__main__':
    apps = {
        '/': home_page,
        '/domain_selection': domain_selection
    }
    start_server(apps, port=8080, debug=True)