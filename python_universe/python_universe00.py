from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import plotly.graph_objects as go
import plotly.utils
import json

# Expanded Python domains and packages
python_universe = {
    "Web Development": [
        "Django", "Flask", "FastAPI", "Pyramid", "Tornado", "Dash",
        "aiohttp", "Bottle", "CherryPy", "Sanic", "Starlette",
        "Web2py", "AIOHTTP", "Quart", "Masonite"
    ],
    "Data Science": [
        "NumPy", "Pandas", "SciPy", "Scikit-learn", "TensorFlow",
        "PyTorch", "Keras", "XGBoost", "LightGBM", "CatBoost",
        "Statsmodels", "NLTK", "Spacy", "Gensim", "H2O"
    ],
    "Data Visualization": [
        "Matplotlib", "Seaborn", "Plotly", "Bokeh", "Altair",
        "Pygal", "Folium", "Dash", "Graphviz", "NetworkX",
        "ggplot", "Plotnine", "Chartify", "Holoviews", "Geoplotlib"
    ],
    "Automation & Testing": [
        "Selenium", "PyAutoGUI", "Robot Framework", "Scrapy", "Beautiful Soup",
        "Pytest", "Unittest", "Behave", "Locust", "Pywinauto",
        "AutoIt", "Rpa Framework", "Mechanize", "Splinter", "Nose"
    ],
    "Game Development": [
        "Pygame", "Panda3D", "Arcade", "Kivy", "Pyglet",
        "Cocos2d", "Ren'Py", "PyOpenGL", "Harfang3D", "Rabbyt",
        "Python-Ogre", "Pygame Zero", "Wasabi2D", "PySDL2", "Arcade"
    ],
    "Desktop Applications": [
        "PyQt", "Tkinter", "wxPython", "PyGObject", "Kivy",
        "PySide", "PySimpleGUI", "Dear PyGui", "Toga", "Wx",
        "Flet", "CustomTkinter", "PyForms", "Wax", "AWT"
    ],
    "System Administration": [
        "Ansible", "Fabric", "Salt", "Puppet", "Chef",
        "Paramiko", "PSUtil", "PyInstaller", "Python-MSI", "WMI",
        "Watchdog", "Schedule", "APScheduler", "Supervisor", "Circus"
    ],
    "Scientific Computing": [
        "SymPy", "BioPython", "Astropy", "PyCBC", "Qiskit",
        "Sage", "PySCF", "Quantum", "MDAnalysis", "ASE",
        "PyMOL", "OpenMM", "DeepChem", "PyCUDA", "Theano"
    ],
    "Document Automation": [
        "PyPDF2", "python-docx", "python-pptx", "ReportLab", "PDFMiner",
        "Camelot", "Tabula-py", "DocxTemplate", "PyMuPDF", "WeasyPrint",
        "Pandoc", "XlsxWriter", "OpenPyXL", "PyDocX", "PDFKit"
    ],
    "HRIS & HRM": [
        "OdooHR", "PyHR", "HR-Python-Suite", "PeopleSoft-Py", "PyPayroll",
        "PyTimesheet", "PyAttendance", "PyRecruitment", "PyPerformance", "PyBenefits",
        "WorkdayAPI", "SAP-HCM-Python", "PyLeave", "PyTraining", "PyCompensation"
    ],
    "CRM & Sales": [
        "SalesforcePy", "HubSpot-Python", "ZohoCRM-Py", "PyDynamics365", "SuiteCRM-Python",
        "FreshworksCRM", "Odoo-CRM", "VTiger-Python", "PipedrivePy", "AgileCRM-Python",
        "InsightlyCRM", "PySugarCRM", "ZenDeskSell", "CloseIO-Python", "NetSuitePy"
    ],
    "Project Management": [
        "Python-Jira", "PyGithub", "Trello-Python", "Asana-Python", "Monday-Python",
        "ClickUp-Python", "PyTeamwork", "Basecamp3-Py", "PyConfluence", "PyRedmine",
        "PyNotion", "PyAzureDevOps", "PyServiceNow", "SmartsheetPython", "PyWrike"
    ],
    "Business Intelligence": [
        "PyTableau", "PowerBI-Python", "PyQlik", "Looker-Python", "Sisense-Py",
        "PyMicroStrategy", "PyDomo", "ThoughtSpot-Py", "PyMetabase", "PyPentaho",
        "PyJasper", "PyBirst", "PyYellowfin", "PySAP-BO", "PyClickhouse"
    ],
    "ERP Integration": [
        "PySAP", "Odoo-Python", "NetSuite-Py", "PyDynamics", "PyOracle-ERP",
        "PyEpicor", "PySage", "PyInfor", "PyAcct", "PyQuickBooks",
        "PyWorkday", "PyPeopleSoft", "PyJDEdwards", "PyIFS", "PyDeltek"
    ],
    "Workflow Automation": [
        "Apache-Airflow", "PyPrefect", "Dagster", "Luigi", "PyKubeflow",
        "PyCelery", "PyDramatiq", "PyRQ", "PyHuey", "PyAPScheduler",
        "PyTaskflow", "PyZeebe", "PyCamunda", "PyN8N", "PyTempo"
    ],
    "Document Management": [
        "PyAlfresco", "PySharePoint", "PyOpenKM", "PyDocuShare", "PyM-Files",
        "PyDocuWare", "PyLaserfiche", "PyOnBase", "PyFileNet", "PyDocStar",
        "PyEfileCabinet", "PyDocuphase", "PyGlobalscape", "PyDoxTG", "PyMasterControl"
    ],
    "Communication & Collaboration": [
        "PySlack", "PyTeams", "PyDiscord", "PyZoom", "PyWebex",
        "PyRocketChat", "PyMattermost", "PyHipChat", "PyFlock", "PyTelegram",
        "PySignal", "PyMatrix", "PyJabber", "PySkype", "PyGoogleChat"
    ]
}

def create_dashboard():
    put_markdown("# Welcome to the Python Universe")
    
    # Domain selector
    selected_domains = select(
        label="Select Domains to View",
        options=list(python_universe.keys()),
        multiple=True,
        value=list(python_universe.keys())  # All domains selected by default
    )
    
    if not selected_domains:
        selected_domains = list(python_universe.keys())
    
    # Filter python_universe based on selected domains
    filtered_universe = {k: python_universe[k] for k in selected_domains}
    
    # Show domains and packages
    put_markdown("## Python Domains and Packages")
    
    for domain, packages in filtered_universe.items():
        put_collapse(f"{domain} ({len(packages)} packages)", [
            put_table([
                [package] for package in packages
            ])
        ])
    
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
    put_markdown("## Domain Statistics")
    
    # Grouped Bar Chart
    fig = go.Figure(data=[
        go.Bar(
            name='Available Packages',
            x=list(domain_stats.keys()),
            y=list(domain_stats.values()),
            text=list(domain_stats.values()),
            textposition='auto',
            marker_color='rgb(55, 83, 109)'
        ),
        go.Bar(
            name='Packages You Know',
            x=list(user_domain_stats.keys()),
            y=list(user_domain_stats.values()),
            text=list(user_domain_stats.values()),
            textposition='auto',
            marker_color='rgb(26, 118, 255)'
        )
    ])
    
    fig.update_layout(
        title="Packages by Domain: Available vs. Known",
        xaxis_title="Domains",
        yaxis_title="Number of Packages",
        height=800,
        barmode='group',
        xaxis={'tickangle': 45},
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
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

if __name__ == '__main__':
    start_server(create_dashboard, port=8080, debug=True)
