# Python Universe Explorer

A dynamic, interactive dashboard for exploring and tracking your Python package knowledge across different domains.

## Overview

Python Universe Explorer is a web-based tool that helps developers visualize and track their experience with Python packages across various domains. It fetches real-world package data from the awesome-python GitHub repository and organizes them into meaningful business and technical domains.

## Features

### 1. Domain Organization
- Automatically categorizes Python packages into real-world application domains
- Includes domains such as:
  - Enterprise Solutions
  - Web Development
  - Data Science & Analytics
  - Database & Storage
  - DevOps & Infrastructure
  - Security & Cryptography
  - System Integration
  - Content Management
  - GUI & Desktop
  - Cloud & Serverless

### 2. Interactive Visualizations
- **Domain Hierarchy Treemap**
  - Visual representation of package distribution across domains
  - Color-coded sections for easy navigation
  - Interactive hover details showing package counts
  - Hierarchical view of domains and their sub-sections

- **Package Statistics Bar Chart**
  - Comparison between available packages and known packages
  - Color-coded bars for easy distinction
  - Interactive tooltips with exact counts
  - Responsive design with rotated labels for better readability

### 3. Package Selection
- Multi-select domain filter
- Checkbox-based package selection
- Track packages you've worked with
- Domain-wise package organization

### 4. Data Management
- Caches fetched data for better performance
- Automatic data refresh capability
- Fallback to cached data when offline

## Installation

1. Download the folder:

2. Install the required dependencies:

pip install pywebio plotly requests beautifulsoup4

3. Run the application:

python python_universe02.py

4. Access the application:
- Open your web browser
- Navigate to: `http://localhost:8080`
- The home page will show the Python Domain Treemap
- Click "Explore Python Domains" to access the domain selection interface

## Usage

The application provides two main interfaces:

1. **Home Page** (`/`)
   - Interactive treemap visualization of Python domains
   - Overview of package distribution
   - Navigation to domain selection

2. **Domain Selection** (`/domain_selection`)
   - Select specific domains to explore
   - View detailed package listings
   - Material Design interface for better user experience

## Technical Details

- Built with PyWebIO for web interface
- Uses Plotly for interactive visualizations
- Material Design-inspired UI components
- Responsive layout for all screen sizes
- Multi-page application structure
- Session-based state management

## Data Sources

- Primary data source: [awesome-python](https://github.com/vinta/awesome-python)
- Package verification: PyPI API

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- awesome-python repository maintainers
- PyWebIO developers
- Plotly team
- Material Design team